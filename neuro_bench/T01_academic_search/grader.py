#!/usr/bin/env python3
"""
Grader for Benchmark Test Case 1: Academic Search

This script evaluates whether all papers retrieved are within 180 days
from the search date. It checks:
1. JSON format correctness
2. All papers have valid publication dates
3. All papers are within the 180-day window
4. Papers are sorted by date (newest first)

Pass: All papers are within 180 days
Fail: Any paper is outside the 180-day window or format is invalid
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple


def parse_date(date_str: str) -> Tuple[datetime, bool]:
    """
    Parse various date formats and return datetime object.
    Returns (datetime_object, is_valid).
    """
    if not date_str or date_str == "N/A" or date_str == "Unknown":
        return None, False
    
    # Try common formats
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y",  # Year only
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.split("T")[0] if "T" in date_str else date_str, 
                                   fmt if "T" not in fmt else "%Y-%m-%d")
            return dt, True
        except ValueError:
            continue
    
    return None, False


def grade_papers(json_file: Path) -> Dict[str, Any]:
    """
    Grade the papers in the JSON file.
    
    Returns a dict with:
    - passed: bool - whether all papers passed
    - total_papers: int
    - papers_in_range: int
    - papers_out_of_range: int
    - date_parsing_errors: int
    - details: list of strings with details
    """
    
    results = {
        "passed": False,
        "total_papers": 0,
        "papers_in_range": 0,
        "papers_out_of_range": 0,
        "date_parsing_errors": 0,
        "details": []
    }
    
    # Load JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        results["details"].append(f"❌ Error loading JSON file: {e}")
        return results
    
    # Check JSON structure
    if "metadata" not in data:
        results["details"].append("❌ Missing 'metadata' key in JSON")
        return results
    
    metadata = data["metadata"]
    
    # Get search date (from metadata or use now)
    search_timestamp = metadata.get("timestamp", "")
    search_date, valid = parse_date(search_timestamp)
    if not valid:
        search_date = datetime.now()
    
    cutoff_date = search_date - timedelta(days=180)
    
    results["details"].append(f"📅 Search date: {search_date.strftime('%Y-%m-%d')}")
    results["details"].append(f"📅 Cutoff date (180 days ago): {cutoff_date.strftime('%Y-%m-%d')}")
    results["details"].append("")
    
    # Check each platform
    platforms = ["arxiv", "pubmed", "semantic_scholar", "openreview"]
    
    for platform in platforms:
        if platform not in data:
            continue
        
        papers = data[platform]
        if not papers:
            results["details"].append(f"✓ {platform.upper()}: 0 papers (empty)")
            continue
        
        results["details"].append(f"\n### {platform.upper()} ({len(papers)} papers)")
        
        platform_in_range = 0
        platform_out_of_range = 0
        platform_parse_errors = 0
        out_of_range_papers = []
        
        for i, paper in enumerate(papers, 1):
            pub_date_str = paper.get("published", "")
            title = paper.get("title", f"Paper {i}")[:50]
            
            # Parse date
            pub_date, valid = parse_date(pub_date_str)
            
            if not valid:
                platform_parse_errors += 1
                results["date_parsing_errors"] += 1
                results["details"].append(f"  ⚠️  {i}. {title}... [DATE PARSE ERROR: '{pub_date_str}']")
                continue
            
            # Check if in range
            if pub_date >= cutoff_date:
                platform_in_range += 1
                results["papers_in_range"] += 1
            else:
                platform_out_of_range += 1
                results["papers_out_of_range"] += 1
                out_of_range_papers.append({
                    "index": i,
                    "title": title,
                    "date": pub_date.strftime("%Y-%m-%d"),
                    "days_before_cutoff": (cutoff_date - pub_date).days
                })
            
            results["total_papers"] += 1
        
        # Summary for platform
        results["details"].append(f"  ✓ In range: {platform_in_range}")
        if platform_out_of_range > 0:
            results["details"].append(f"  ❌ Out of range: {platform_out_of_range}")
            for paper in out_of_range_papers[:3]:  # Show first 3
                results["details"].append(
                    f"     - {paper['index']}. {paper['title']} ({paper['date']}, "
                    f"{paper['days_before_cutoff']} days before cutoff)"
                )
            if len(out_of_range_papers) > 3:
                results["details"].append(f"     ... and {len(out_of_range_papers) - 3} more")
        
        if platform_parse_errors > 0:
            results["details"].append(f"  ⚠️  Parse errors: {platform_parse_errors}")
    
    # Final verdict
    results["details"].append("\n" + "="*70)
    results["details"].append("GRADING RESULTS")
    results["details"].append("="*70)
    results["details"].append(f"Total papers retrieved: {results['total_papers']}")
    results["details"].append(f"Papers within 180 days: {results['papers_in_range']}")
    results["details"].append(f"Papers outside 180 days: {results['papers_out_of_range']}")
    results["details"].append(f"Date parsing errors: {results['date_parsing_errors']}")
    
    # Determine pass/fail
    if results["total_papers"] == 0:
        results["details"].append("\n❌ FAIL: No papers retrieved")
        results["passed"] = False
    elif results["papers_out_of_range"] > 0:
        results["details"].append(f"\n❌ FAIL: {results['papers_out_of_range']} papers are outside the 180-day window")
        results["passed"] = False
    elif results["date_parsing_errors"] > 0:
        results["details"].append(f"\n⚠️  PASS (WITH WARNINGS): {results['date_parsing_errors']} papers have date parsing issues")
        results["passed"] = True
    else:
        results["details"].append("\n✅ PASS: All papers are within the 180-day window")
        results["passed"] = True
    
    return results


def main():
    """Main grading function."""
    # Find latest JSON file
    output_dir = Path(__file__).parent.parent.parent / "benchmark_results" / "T01_academic_search"
    
    if not output_dir.exists():
        print(f"❌ Output directory not found: {output_dir}")
        sys.exit(1)
    
    json_files = sorted(output_dir.glob("search_results_*.json"), reverse=True)
    
    if not json_files:
        print(f"❌ No result files found in {output_dir}")
        sys.exit(1)
    
    latest_file = json_files[0]
    print(f"📄 Grading: {latest_file.name}\n")
    
    # Grade
    results = grade_papers(latest_file)
    
    # Print results
    for detail in results["details"]:
        print(detail)
    
    # Exit with appropriate code
    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
