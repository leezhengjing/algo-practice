#!/usr/bin/env python3
"""
Test runner with detailed output for development and debugging.
Shows pass/fail status, errors, and expected vs actual output.
"""

import json
import os
import sys
from pathlib import Path

def find_project_root():
    """Find the project root directory (contains problems/ and test_runner/)."""
    current = Path.cwd()
    
    # Check current directory first
    if (current / "problems").exists() and (current / "test_runner").exists():
        return current
    
    # Search upwards for project root
    for parent in current.parents:
        if (parent / "problems").exists() and (parent / "test_runner").exists():
            return parent
    
    # If not found, assume script is in project root
    script_dir = Path(__file__).parent
    if (script_dir / "problems").exists() and (script_dir / "test_runner").exists():
        return script_dir
    
    raise FileNotFoundError("Could not find project root directory with 'problems/' and 'test_runner/' folders")

# Change to project root directory
project_root = find_project_root()
os.chdir(project_root)
print(f"📍 Working directory: {project_root}")

# Now import the test runners (after changing directory)
from test_runner.run_python import run_python
from test_runner.run_cpp import run_cpp
from test_runner.run_js import run_js

LANG_RUNNERS = {
    "py": run_python,
    "cpp": run_cpp,
    "js": run_js,
}

LANG_NAMES = {
    "py": "Python",
    "cpp": "C++",
    "js": "JavaScript",
}

def run_tests_verbose():
    """Run tests with verbose output for debugging."""
    
    # If a specific problem is provided as argument, test only that
    if len(sys.argv) > 1:
        problems_to_test = [sys.argv[1]]
        print(f"🎯 Testing specific problem: {problems_to_test[0]}")
    else:
        # Find all problems recursively
        problems_to_test = []
        for root, dirs, files in os.walk("problems"):
            # Skip the root problems directory itself
            if root == "problems":
                continue
            # Check if this directory contains tests.json
            if "tests.json" in files:
                problem_name = os.path.relpath(root, "problems")
                problems_to_test.append(problem_name)
        
        print(f"🚀 Testing all {len(problems_to_test)} problems")
    
    print("=" * 80)
    
    total_tests = 0
    total_passed = 0
    
    for problem in sorted(problems_to_test):
        problem_path = os.path.join("problems", problem)
        if not os.path.isdir(problem_path):
            print(f"⚠️  {problem}: Directory not found")
            continue
        
        tests_path = os.path.join(problem_path, "tests.json")
        if not os.path.exists(tests_path):
            print(f"⚠️  {problem}: No tests.json found")
            continue
        
        # Load test cases
        try:
            with open(tests_path) as f:
                tests_data = json.load(f)
        except Exception as e:
            print(f"❌ {problem}: Error loading tests.json: {e}")
            continue
        
        # Skip if no tests (for templates/snippets)
        if not tests_data.get("tests") or len(tests_data["tests"]) == 0:
            template_type = tests_data.get("type", "snippet")
            description = tests_data.get("description", "No description")
            print(f"📝 {problem}: {template_type.title()} - {description}")
            continue
        
        print(f"\n📁 Problem: {problem}")
        print("-" * 60)
        
        # Test each language
        for ext, runner in LANG_RUNNERS.items():
            lang_name = LANG_NAMES[ext]
            code_path = os.path.join(problem_path, f"attempt.{ext}")
            
            if not os.path.exists(code_path):
                print(f"  {lang_name:12} | ⚪ Missing")
                continue
            
            # Run all test cases for this language
            passed_tests = 0
            failed_tests = []
            
            for i, test_case in enumerate(tests_data["tests"]):
                total_tests += 1
                output, error = runner(code_path, test_case["input"])
                
                if error:
                    failed_tests.append(f"Test {i+1}: Runtime error - {error}")
                elif output is None:
                    failed_tests.append(f"Test {i+1}: No output returned")
                elif output.strip() != test_case["output"].strip():
                    failed_tests.append(f"Test {i+1}: Output mismatch")
                    failed_tests.append(f"    Expected: {repr(test_case['output'])}")
                    failed_tests.append(f"    Got:      {repr(output)}")
                else:
                    passed_tests += 1
                    total_passed += 1
            
            # Print result for this language
            total_lang_tests = len(tests_data["tests"])
            if passed_tests == total_lang_tests:
                print(f"  {lang_name:12} | ✅ Pass ({passed_tests}/{total_lang_tests})")
            else:
                print(f"  {lang_name:12} | ❌ Fail ({passed_tests}/{total_lang_tests})")
                for failure in failed_tests:
                    print(f"                   {failure}")
    
    print("\n" + "=" * 80)
    print(f"📊 Summary: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"💥 {total_tests - total_passed} tests failed")
        return 1

if __name__ == "__main__":
    exit_code = run_tests_verbose()
    sys.exit(exit_code)
