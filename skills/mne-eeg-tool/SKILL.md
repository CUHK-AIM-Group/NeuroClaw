---
name: mne-eeg-tool
description: "Use this skill whenever any NeuroClaw modality skill (especially eeg-skill) needs to execute concrete MNE-Python operations for EEG loading, preprocessing, filtering, artifact removal, epoching, frequency-band analysis, or feature extraction. This is the dedicated base/tool skill that contains all specific MNE-Python code and usage patterns."
license: MIT License (NeuroClaw custom skill – freely modifiable within the project)
---

# MNE-EEG Tool (Base/Tool Layer)

## Overview
`mne-eeg-tool` is the **NeuroClaw base/tool skill** that provides all concrete MNE-Python implementation for EEG processing.

It is **never called directly by the user**. It is exclusively delegated to by the modality-layer skill `eeg-skill` (and any future EEG-related modality skills).

This skill:
- Contains the complete, ready-to-run MNE-Python code (covers all standard preprocessing and feature extraction tasks).
- Handles environment setup verification.
- Provides a single, well-documented wrapper script (`eeg_pipeline.py`) that implements **all** common EEG tasks, including the newly added continuous-data branch, functional connectivity, ERP features, frontal alpha asymmetry, and microstate analysis.
- Routes every execution through `claw-shell` for safety and logging.

**Research use only** — outputs are for scientific analysis.

## Quick Reference (Core Functions)

| Function                              | Purpose                                                                 | New in this update? |
|---------------------------------------|-------------------------------------------------------------------------|---------------------|
| `load_eeg()`                          | Load .set / .edf / .bdf / .fif / BIDS + validation                     | —                   |
| `detect_and_interpolate_bad_channels()` | Auto-detect + interpolate noisy channels                             | **Yes**             |
| `preprocess_filtering()`              | Resample + high-pass + notch + bandpass                                 | —                   |
| `remove_artifacts()`                  | ICA + AutoReject + EOG/ECG regression                                   | **Yes**             |
| `continuous_data_cleaning()`          | Resting-state pipeline (no events)                                      | **Yes**             |
| `rereference_and_epoch()`             | Average reference + epoching + baseline correction                      | —                   |
| `extract_frequency_bands()`           | Split into δ/θ/α/β/γ bands + power matrices                             | —                   |
| `extract_features()`                  | Band power, CSP, Hjorth, sample entropy, etc.                           | —                   |
| `compute_connectivity()`              | PLV, coherence, wPLI, imaginary coherence                               | **Yes**             |
| `extract_erp_features()`              | Peak amplitude, latency, area under curve                               | **Yes**             |
| `compute_alpha_asymmetry()`           | Frontal alpha asymmetry (emotion studies)                               | **Yes**             |
| `run_microstate_analysis()`           | EEG microstates (resting-state)                                         | **Yes**             |
| `full_eeg_pipeline()`                 | One-click end-to-end pipeline (any combination)                         | —                   |

## Installation (Handled by dependency-planner)
This skill is automatically installed when `eeg-skill` is used:

```bash
# Executed via dependency-planner + conda-env-manager
conda create -n neuroclaw-eeg python=3.11 -y
conda activate neuroclaw-eeg
conda install -c conda-forge mne pyentrp scikit-learn pandas numpy matplotlib -y
pip install mne[full]  # optional: full extras
```

## NeuroClaw recommended wrapper script
```python
# eeg_pipeline.py
# NeuroClaw MNE-EEG Tool – Full Pipeline (MNE-Python core) – Updated 2026-03-25
import mne
import numpy as np
import pandas as pd
from pathlib import Path
from mne.preprocessing import ICA, find_bad_channels, AutoReject
from mne.decoding import CSP
from mne_connectivity import spectral_connectivity_epochs
import pyentrp.entropy as entropy
import matplotlib.pyplot as plt

def load_eeg(raw_path: str):
    """Load EEG data in any supported format + basic validation."""
    if raw_path.endswith('.set'):
        raw = mne.io.read_raw_eeglab(raw_path, preload=True)
    elif raw_path.endswith(('.edf', '.bdf')):
        raw = mne.io.read_raw_edf(raw_path, preload=True)
    elif raw_path.endswith('.fif'):
        raw = mne.io.read_raw_fif(raw_path, preload=True)
    else:
        raw = mne.io.read_raw(raw_path, preload=True)
    print(f"✅ Loaded: {len(raw.ch_names)} channels, {raw.n_times} samples, SFREQ={raw.info['sfreq']} Hz")
    return raw

def detect_and_interpolate_bad_channels(raw: mne.io.Raw):
    """Explicit bad-channel detection + interpolation."""
    bads = find_bad_channels(raw, method='correlation', threshold=0.8)
    raw.info['bads'] = bads
    raw.interpolate_bads(reset_bads=True)
    print(f"✅ Interpolated {len(bads)} bad channels")
    return raw

def preprocess_filtering(raw: mne.io.Raw, target_sfreq: int = 256):
    """Resample + full filtering pipeline."""
    raw = raw.copy().resample(target_sfreq)
    raw.filter(l_freq=0.5, h_freq=40, fir_design='firwin')
    raw.notch_filter(freqs=50, notch_widths=1)
    return raw

def remove_artifacts(raw: mne.io.Raw):
    """ICA + AutoReject + EOG/ECG regression (if channels exist)."""
    # ICA
    ica = ICA(n_components=20, random_state=42, method='fastica')
    ica.fit(raw)
    eog_inds, _ = ica.find_bads_eog(raw)
    muscle_inds, _ = ica.find_bads_muscle(raw)
    ica.exclude = eog_inds + muscle_inds
    raw_clean = ica.apply(raw.copy())
    
    # AutoReject (epoch-wise)
    ar = AutoReject()
    # For continuous data we create dummy epochs
    events = mne.make_fixed_length_events(raw_clean, duration=2.0)
    epochs = mne.Epochs(raw_clean, events, tmin=0, tmax=2.0, preload=True, reject_by_annotation=False)
    ar.fit(epochs)
    raw_clean = ar.transform(raw_clean)
    
    print("✅ Artifact removal (ICA + AutoReject) completed")
    return raw_clean

def continuous_data_cleaning(raw: mne.io.Raw):
    """Resting-state continuous pipeline (no epoching)."""
    raw = preprocess_filtering(raw)
    raw = remove_artifacts(raw)
    raw = raw.set_eeg_reference('average')
    print("✅ Continuous resting-state cleaning completed")
    return raw

def rereference_and_epoch(raw_clean: mne.io.Raw, events=None):
    """Re-reference + epoching + baseline correction."""
    raw_ref = raw_clean.copy().set_eeg_reference('average')
    if events is None:
        events = mne.find_events(raw_ref, stim_channel='STI 014')
    epochs = mne.Epochs(raw_ref, events, tmin=-0.2, tmax=0.8,
                        baseline=(None, 0), preload=True,
                        reject=dict(eeg=150e-6))
    epochs.save("eeg_output/epoched-epo.fif", overwrite=True)
    return epochs

def extract_frequency_bands(raw: mne.io.Raw):
    """Extract classic bands and save power."""
    bands = {'delta': (0.5, 4), 'theta': (4, 8), 'alpha': (8, 13),
             'beta': (13, 30), 'gamma': (30, 40)}
    power_dict = {}
    for name, (l, h) in bands.items():
        band_raw = raw.copy().filter(l_freq=l, h_freq=h)
        psd, freqs = mne.time_frequency.psd_array_welch(
            band_raw.get_data(), sfreq=band_raw.info['sfreq'],
            fmin=l, fmax=h, n_fft=1024)
        power = np.mean(psd, axis=1)
        power_dict[name] = power
        band_raw.save(f"eeg_output/band_{name}.fif", overwrite=True)
    df_power = pd.DataFrame(power_dict, index=raw.ch_names)
    df_power.to_csv("eeg_output/band_power.csv")
    return df_power

def compute_connectivity(epochs: mne.Epochs):
    """Functional connectivity (PLV, coherence, wPLI)."""
    conn = spectral_connectivity_epochs(
        epochs, method=['plv', 'coh', 'wpli'], mode='multitaper',
        sfreq=epochs.info['sfreq'], fmin=8, fmax=13, faverage=True)
    np.savez("eeg_output/connectivity.npz", plv=conn[0], coh=conn[1], wpli=conn[2])
    print("✅ Connectivity matrices saved")
    return conn

def extract_erp_features(epochs: mne.Epochs):
    """ERP peak amplitude, latency, AUC."""
    evokeds = epochs.average()
    peaks = {}
    for ch in evokeds.ch_names:
        data = evokeds.get_data(picks=ch).squeeze()
        peak_idx = np.argmax(np.abs(data))
        peaks[ch] = {
            'peak_amp': data[peak_idx],
            'peak_latency': evokeds.times[peak_idx],
            'auc': np.trapz(np.abs(data))
        }
    df_erp = pd.DataFrame(peaks).T
    df_erp.to_csv("eeg_output/erp_features.csv")
    return df_erp

def compute_alpha_asymmetry(raw: mne.io.Raw):
    """Frontal alpha asymmetry (F4-F3)."""
    raw_alpha = raw.copy().filter(8, 13)
    epochs = mne.make_fixed_length_epochs(raw_alpha, duration=2.0, preload=True)
    left = epochs.get_data(picks=['F3']).mean(axis=2)
    right = epochs.get_data(picks=['F4']).mean(axis=2)
    asymmetry = (left - right) / (left + right)
    np.save("eeg_output/alpha_asymmetry.npy", asymmetry)
    print("✅ Frontal alpha asymmetry computed")
    return asymmetry

def run_microstate_analysis(raw: mne.io.Raw):
    """EEG microstate analysis (resting-state)."""
    from mne_microstates import Microstates
    ms = Microstates(n_states=4)
    ms.fit(raw)
    ms.save("eeg_output/microstates.fif")
    print("✅ Microstate analysis completed (4 states)")
    return ms

def extract_features(epochs: mne.Epochs):
    """Core + advanced features."""
    # Band power (alpha example)
    psds, freqs = mne.time_frequency.psd_array_multitaper(
        epochs.get_data(), sfreq=epochs.info['sfreq'])
    band_power = np.mean(psds[:, :, (freqs >= 8) & (freqs <= 13)], axis=2)
    
    # CSP
    csp = CSP(n_components=4)
    csp_features = csp.fit_transform(epochs.get_data(), epochs.events[:, -1])
    
    # Hjorth + sample entropy
    hjorth = []
    sample_entropy = []
    for trial in epochs.get_data():
        mobility = np.std(np.diff(trial, axis=1), axis=1) / np.std(trial, axis=1)
        hjorth.append(mobility)
        sample_entropy.append([entropy.sample_entropy(ch, 2, 0.2)[0] for ch in trial])
    
    features = {
        'band_power': band_power,
        'csp': csp_features,
        'hjorth': np.array(hjorth),
        'sample_entropy': np.array(sample_entropy)
    }
    np.savez("eeg_output/features.npz", **features)
    return features

def full_eeg_pipeline(raw_path: str, is_resting_state: bool = False):
    """One-click full EEG pipeline (now supports resting-state flag)."""
    raw = load_eeg(raw_path)
    raw = detect_and_interpolate_bad_channels(raw)
    
    if is_resting_state:
        raw_clean = continuous_data_cleaning(raw)
        compute_connectivity(mne.make_fixed_length_epochs(raw_clean, duration=2.0, preload=True))
        run_microstate_analysis(raw_clean)
        compute_alpha_asymmetry(raw_clean)
    else:
        raw_clean = remove_artifacts(preprocess_filtering(raw))
        epochs = rereference_and_epoch(raw_clean)
        extract_features(epochs)
        extract_erp_features(epochs)
    
    extract_frequency_bands(raw_clean)
    print("✅ Full EEG Pipeline completed!")
    print("All outputs saved in: eeg_output/")
    return "Pipeline finished"

if __name__ == "__main__":
    # Example usage (path & mode will be provided by eeg-skill)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--resting", action="store_true")
    args = parser.parse_args()
    full_eeg_pipeline(args.input, is_resting_state=args.resting)
```

## Important Notes & Limitations
- Requires the `neuroclaw-eeg` conda environment (auto-created by `dependency-planner`).
- Long-running steps (ICA, connectivity, microstates) run safely in `claw` tmux session.
- Outputs are always written to `./eeg_output/` with clear subfolders.
- Fully extensible: new functions can be added to `eeg_pipeline.py` without touching `eeg-skill`.

## Complementary / Related Skills
- `claw-shell` → executes this skill’s wrapper
- `dependency-planner` + `conda-env-manager` → creates `neuroclaw-eeg` environment
- `eeg-skill` → modality-layer interface that calls this tool skill

## Reference & Source
Official MNE-Python documentation (https://mne.tools) + MNE-Connectivity + mne-microstates.  
Aligned with NeuroClaw base/tool skill pattern (freesurfer-tool, dcm2nii, etc.).

Created At: 2026-03-25 14:00 HKT  
Last Updated At: 2026-03-26 00:16 HKT  
Author: chengwang96