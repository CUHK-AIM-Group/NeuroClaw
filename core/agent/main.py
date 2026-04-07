"""
NeuroClaw Core Agent — LLM conversation loop and tool-call dispatcher.

Architecture
------------
  AgentSession
    │
    ├─ SkillLoader        loads skills/*/SKILL.md, registers tools
    ├─ ToolRuntime        executes handler.js / Python handlers
    ├─ SessionManager     context window, persistence, compression
    └─ LLMBackend         OpenAI / Anthropic / local model adapter

This module is the self-contained replacement for OpenClaw's agent loop.
Messaging connectors (WhatsApp, Slack, Telegram) are intentionally excluded;
see core/config/features.json to audit disabled features.

Usage
-----
    # Interactive REPL
    python core/agent/main.py

    # Browser-based Web UI (served on http://localhost:7080 by default)
    python core/agent/main.py --web [--port 7080] [--host 127.0.0.1]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
ENV_FILE = REPO_ROOT / "neuroclaw_environment.json"
FEATURES_FILE = REPO_ROOT / "core" / "config" / "features.json"


# ── Environment bootstrap ──────────────────────────────────────────────────────

def load_environment() -> dict:
    """
    Load neuroclaw_environment.json and export toolchain environment variables.

    Called automatically at session start (as specified in SOUL.md).
    If the file does not exist, the agent will prompt the user to run the
    installer before proceeding.
    """
    if not ENV_FILE.exists():
        return {}

    with ENV_FILE.open() as f:
        env = json.load(f)

    _export_toolchain_env(env)
    return env


def _export_toolchain_env(env: dict) -> None:
    """
    Export FSLDIR, FREESURFER_HOME, CUDA_VISIBLE_DEVICES, etc.
    into the current process environment so all child processes inherit them.
    """
    toolchain = env.get("toolchain", {})
    if toolchain.get("fsl_home"):
        os.environ.setdefault("FSLDIR", toolchain["fsl_home"])
        fsl_bin = str(Path(toolchain["fsl_home"]) / "bin")
        _prepend_path(fsl_bin)

    if toolchain.get("freesurfer_home"):
        os.environ.setdefault("FREESURFER_HOME", toolchain["freesurfer_home"])
        fs_bin = str(Path(toolchain["freesurfer_home"]) / "bin")
        _prepend_path(fs_bin)

    cuda = env.get("cuda", {})
    device = cuda.get("device", "")
    if device and device.startswith("cuda:"):
        gpu_index = device.split(":")[1]
        os.environ.setdefault("CUDA_VISIBLE_DEVICES", gpu_index)


def _prepend_path(directory: str) -> None:
    current = os.environ.get("PATH", "")
    if directory not in current.split(os.pathsep):
        os.environ["PATH"] = directory + os.pathsep + current


# ── Feature gate ───────────────────────────────────────────────────────────────

def is_feature_enabled(category: str, name: str) -> bool:
    """Return True if features.json marks category.name as enabled."""
    if not FEATURES_FILE.exists():
        return True  # permissive default if features file is missing
    with FEATURES_FILE.open() as f:
        features = json.load(f)
    return features.get(category, {}).get(name, {}).get("enabled", True)


# ── LLM backend factory ────────────────────────────────────────────────────────

def build_llm_client(env: dict) -> Any:
    """
    Return a thin LLM client object based on env['llm_backend'].
    Raises RuntimeError if the required library is not installed or
    the provider is not enabled in features.json.
    """
    llm_cfg = env.get("llm_backend", {})
    provider = llm_cfg.get("provider", "openai")

    if not is_feature_enabled("llm_backends", provider):
        raise RuntimeError(
            f"LLM provider '{provider}' is disabled in features.json."
        )

    if provider == "openai":
        return _build_openai_client(llm_cfg)
    if provider == "anthropic":
        return _build_anthropic_client(llm_cfg)
    if provider == "local":
        return _build_local_client(llm_cfg)

    raise RuntimeError(f"Unknown LLM provider: {provider}")


def _build_openai_client(cfg: dict):
    try:
        import openai  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "openai package not installed. Run: pip install openai"
        ) from exc
    key_env = cfg.get("api_key_env", "OPENAI_API_KEY")
    api_key = os.environ.get(key_env, "")
    return openai.OpenAI(api_key=api_key)


def _build_anthropic_client(cfg: dict):
    try:
        import anthropic  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "anthropic package not installed. Run: pip install anthropic"
        ) from exc
    key_env = cfg.get("api_key_env", "ANTHROPIC_API_KEY")
    api_key = os.environ.get(key_env, "")
    return anthropic.Anthropic(api_key=api_key)


def _build_local_client(cfg: dict):
    """Return a minimal dict config; actual HTTP calls are handled by ToolRuntime."""
    return {
        "provider": "local",
        "endpoint": cfg.get("local_endpoint", "http://localhost:11434"),
        "model": cfg.get("model", "llama3:8b"),
    }


# ── Agent session ──────────────────────────────────────────────────────────────

class AgentSession:
    """
    Minimal NeuroClaw agent session.

    Responsibilities:
    - Bootstrap environment (load_environment)
    - Load skills via SkillLoader
    - Maintain conversation history
    - Route tool calls to ToolRuntime
    - Stream responses from the LLM backend
    """

    def __init__(self, workspace: Path | None = None) -> None:
        self.workspace = workspace or REPO_ROOT
        self.env = load_environment()
        self.history: list[dict] = []
        self._llm: Any = None

    # ── Public API for external callers (e.g. the web server) ──────────────────

    def set_llm_client(self, client: Any) -> None:
        """
        Attach an already-constructed LLM client to this session.

        Prefer calling this over accessing ``self._llm`` directly so that
        the internal field can be renamed without breaking callers.
        """
        self._llm = client

    def start(self) -> None:
        """Interactive REPL — called by main.py."""
        if not ENV_FILE.exists():
            self._prompt_setup()
            return

        import importlib.util as _ilu

        # SkillLoader lives in core/skill-loader/ (hyphen) so we must use
        # importlib rather than a regular package import.
        _loader_mod = _ilu.spec_from_file_location(
            "neuroclaw_skill_loader",
            REPO_ROOT / "core" / "skill-loader" / "loader.py",
        )
        if _loader_mod is None or _loader_mod.loader is None:
            raise RuntimeError("Cannot find core/skill-loader/loader.py")
        _m = __import__("importlib").util.module_from_spec(_loader_mod)
        _loader_mod.loader.exec_module(_m)
        SkillLoader = _m.SkillLoader

        from core.session.manager import SessionManager  # type: ignore

        loader = SkillLoader(self.workspace / "skills")
        skills = loader.load_all()

        manager = SessionManager(env=self.env)
        self._llm = build_llm_client(self.env)

        system_prompt = self._build_system_prompt(skills)
        self.history = [{"role": "system", "content": system_prompt}]

        print("NeuroClaw ready. Type your message (Ctrl-C to exit).\n")
        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nSession ended.")
                break
            if not user_input:
                continue

            self.history.append({"role": "user", "content": user_input})
            response = self._chat()
            print(f"\nNeuroClaw: {response}\n")
            self.history.append({"role": "assistant", "content": response})
            manager.maybe_compress(self.history)

    def _chat(self) -> str:
        """Send history to LLM and return response text (simplified, no streaming)."""
        provider = self.env.get("llm_backend", {}).get("provider", "openai")
        model = self.env.get("llm_backend", {}).get("model", "gpt-4o")

        if provider == "openai":
            resp = self._llm.chat.completions.create(
                model=model, messages=self.history
            )
            return resp.choices[0].message.content or ""

        if provider == "anthropic":
            system_msg = next(
                (m["content"] for m in self.history if m["role"] == "system"), ""
            )
            user_msgs = [m for m in self.history if m["role"] != "system"]
            resp = self._llm.messages.create(
                model=model,
                max_tokens=4096,
                system=system_msg,
                messages=user_msgs,
            )
            return resp.content[0].text if resp.content else ""

        if provider == "local":
            import urllib.request  # stdlib only

            endpoint = self._llm["endpoint"]
            payload = json.dumps(
                {"model": self._llm["model"], "messages": self.history, "stream": False}
            ).encode()
            req = urllib.request.Request(
                f"{endpoint}/api/chat",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
            return data.get("message", {}).get("content", "")

        return "[Agent: LLM backend not configured]"

    def _build_system_prompt(self, skills: list[dict]) -> str:
        soul_path = self.workspace / "SOUL.md"
        soul = soul_path.read_text() if soul_path.exists() else ""
        skill_names = ", ".join(s.get("name", "") for s in skills)
        return f"{soul}\n\nLoaded skills: {skill_names}"

    @staticmethod
    def _prompt_setup() -> None:
        print(
            "neuroclaw_environment.json not found.\n"
            "Please run the installer first:\n\n"
            "    python installer/setup.py\n"
        )


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="NeuroClaw — neuroscience AI assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python core/agent/main.py                # interactive REPL\n"
            "  python core/agent/main.py --web          # browser GUI on :7080\n"
            "  python core/agent/main.py --web --port 8080"
        ),
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Start the browser-based Web UI instead of the interactive REPL.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7080,
        metavar="PORT",
        help="Port for the Web UI (default: 7080). Ignored unless --web is set.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        metavar="HOST",
        help="Bind host for the Web UI (default: 127.0.0.1). Ignored unless --web is set.",
    )
    args = parser.parse_args()

    if args.web:
        # Import lazily so FastAPI/uvicorn are only required when --web is used
        import importlib.util as _ilu

        _srv_path = Path(__file__).parent.parent / "web" / "server.py"
        _spec = _ilu.spec_from_file_location("neuroclaw_web_server", _srv_path)
        if _spec is None or _spec.loader is None:
            print(f"ERROR: Cannot find web server at {_srv_path}", file=sys.stderr)
            sys.exit(1)
        _srv_mod = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_srv_mod)  # type: ignore[union-attr]
        _srv_mod.run_server(host=args.host, port=args.port)
    else:
        session = AgentSession()
        session.start()


if __name__ == "__main__":
    main()
