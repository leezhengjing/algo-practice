#!/usr/bin/env python3
"""
Quick test runner for the current problem directory.
Run this from any problem directory to test just that problem.
"""

import os
import sys
from pathlib import Path

# Find project root
current = Path.cwd()
project_root = None

# Check if we're already in project root
if (current / "test_verbose.py").exists():
    project_root = current
else:
    # Search upwards for project root
    for parent in current.parents:
        if (parent / "test_verbose.py").exists():
            project_root = parent
            break

if not project_root:
    print("❌ Could not find project root with test_verbose.py")
    sys.exit(1)

# Get the relative path from problems/
try:
    relative_path = current.relative_to(project_root / "problems")
    problem_name = str(relative_path)
except ValueError:
    print("❌ Not in a problems subdirectory")
    sys.exit(1)

# Change to project root and run test
os.chdir(project_root)
os.system(f"python3 test_verbose.py {problem_name}")
