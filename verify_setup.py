#!/usr/bin/env python3
"""
Setup Verification Script for Probabilistic MaxSAT Lab

Run this script to verify that everything is working correctly.
Usage: python3 verify_setup.py
"""

import os
import sys

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70 + "\n")

def check_item(description, condition):
    """Check an item and print result."""
    status = "✅" if condition else "❌"
    print(f"{status} {description}")
    return condition

def main():
    """Run all verification checks."""
    print_header("🔍 Probabilistic MaxSAT Lab - Setup Verification")
    
    all_checks_passed = True
    
    # Check Python version
    print_header("1. Python Version")
    major, minor = sys.version_info[:2]
    python_ok = major == 3 and minor >= 7
    all_checks_passed &= check_item(
        f"Python version {major}.{minor} (need 3.7+)",
        python_ok
    )
    
    # Check required files exist
    print_header("2. Core Files")
    required_files = [
        "probabilistic_maxsat_solver.py",
        "util.py",
        "visualizer.py",
        "exploration_notebook.py",
        "README.md",
        "INSTRUCTIONS.md",
        "QUICKSTART.md",
    ]
    
    for filename in required_files:
        exists = os.path.exists(filename)
        all_checks_passed &= check_item(
            f"File exists: {filename}",
            exists
        )
    
    # Check problem files
    print_header("3. Problem Files")
    problems_dir = "problems"
    if os.path.exists(problems_dir):
        problem_files = [f for f in os.listdir(problems_dir) if f.endswith('.txt')]
        problems_ok = len(problem_files) >= 5
        all_checks_passed &= check_item(
            f"Found {len(problem_files)} problem files (need at least 5)",
            problems_ok
        )
        
        # Check for key problems
        key_problems = ["hermione.txt", "simple_2vars.txt", "conflicting.txt"]
        for prob in key_problems:
            exists = os.path.exists(os.path.join(problems_dir, prob))
            all_checks_passed &= check_item(
                f"Key problem: {prob}",
                exists
            )
    else:
        all_checks_passed = False
        check_item("Problems directory exists", False)
    
    # Check results directory
    print_header("4. Results Directory")
    results_ok = os.path.exists("results")
    all_checks_passed &= check_item(
        "Results directory exists",
        results_ok
    )
    
    # Try importing modules
    print_header("5. Module Imports")
    try:
        from util import Problem, Atom, Clause
        all_checks_passed &= check_item("Import util module", True)
    except Exception as e:
        all_checks_passed = False
        check_item(f"Import util module (Error: {e})", False)
    
    try:
        from probabilistic_maxsat_solver import hit_and_run
        all_checks_passed &= check_item("Import solver module", True)
    except Exception as e:
        all_checks_passed = False
        check_item(f"Import solver module (Error: {e})", False)
    
    # Try running a simple problem
    print_header("6. Functional Test")
    try:
        from util import Problem
        from probabilistic_maxsat_solver import hit_and_run
        
        hermione_path = os.path.join(problems_dir, "hermione.txt")
        if os.path.exists(hermione_path):
            problem = Problem(hermione_path)
            check_item(f"Load problem ({len(problem.clauses)} clauses)", True)
            
            # Quick test with few iterations
            solution = hit_and_run(problem, iterations=100, verbose=False)
            score = problem.evaluate(solution)
            
            # Check solution is valid
            valid = all(0 <= v <= 1 for v in solution.values())
            all_checks_passed &= check_item(
                f"Generate valid solution (score: {score:.1f})",
                valid
            )
        else:
            all_checks_passed = False
            check_item("Hermione problem not found for testing", False)
            
    except Exception as e:
        all_checks_passed = False
        check_item(f"Functional test (Error: {e})", False)
        import traceback
        traceback.print_exc()
    
    # Final summary
    print_header("📊 Verification Summary")
    
    if all_checks_passed:
        print("🎉 SUCCESS! All checks passed!")
        print("\nYour setup is ready to use. Students can:")
        print("  1. Run: python3 probabilistic_maxsat_solver.py")
        print("  2. Read: README.md, QUICKSTART.md, INSTRUCTIONS.md")
        print("  3. Explore: python3 exploration_notebook.py")
        print("  4. Visualize: python3 visualizer.py problems/hermione.txt")
        print("\nHappy teaching! 🚀")
        return 0
    else:
        print("⚠️  ISSUES DETECTED!")
        print("\nSome checks failed. Please review the errors above.")
        print("\nCommon fixes:")
        print("  - Make sure you're in the ProbabilisticMaxSAT directory")
        print("  - Check that all files were copied correctly")
        print("  - Verify Python version is 3.7 or higher")
        print("\nFor help, see INSTRUCTOR_NOTES.md")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

