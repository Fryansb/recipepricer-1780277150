#!/usr/bin/env python3
"""
Validate that research output meets minimum depth requirements
(400-800 lines of substantive content)
"""

import sys
import re
from pathlib import Path

def count_substantive_lines(filepath):
    """Count lines that are not empty or just whitespace/comments"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        return 0
    
    count = 0
    for line in lines:
        stripped = line.strip()
        # Skip empty lines
        if not stripped:
            continue
        # Skip lines that are just markdown headers (optional - could count them)
        # if stripped.startswith('#'):
        #     continue
        # Skip lines that are just HTML comments
        if stripped.startswith('<!--') and stripped.endswith('-->'):
            continue
        count += 1
    return count

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_research_depth.py <research_file.md>")
        sys.exit(1)
    
    research_file = Path(sys.argv[1])
    line_count = count_substantive_lines(research_file)
    
    print(f"Research file: {research_file}")
    print(f"Substantive lines: {line_count}")
    
    if line_count < 400:
        print(f"ERROR: Research too shallow ({line_count} < 400 lines)")
        sys.exit(1)
    elif line_count > 800:
        print(f"WARNING: Research quite deep ({line_count} > 800 lines) - consider if appropriate")
    else:
        print(f"SUCCESS: Research depth within target range (400-800 lines)")
        sys.exit(0)

if __name__ == "__main__":
    main()