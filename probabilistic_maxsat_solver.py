"""
=== Probabilistic MaxSAT Solver ===

Welcome to the world of fuzzy logic and probabilistic reasoning!

In this lab, you'll implement the Hit-and-Run algorithm to solve
Probabilistic MaxSAT problems, where variables take values in [0,1]
instead of just {0,1}.

=== Your Task ===

Complete the hit_and_run() function below. The algorithm should:
1. Start with a random point in [0,1]^n
2. Pick a random direction
3. Find the valid range along that direction (staying in [0,1]^n)
4. Sample a new point along that direction
5. Evaluate and keep track of the best solution found
6. Repeat!

=== Tips ===

- The evaluate() method gives you the total weighted satisfaction
- All variables must stay in [0,1] at all times
- You can accept only improving moves, or use simulated annealing
- Don't be afraid to experiment!

=== Getting Started ===

Run this file to test your implementation:
    python3 probabilistic_maxsat_solver.py

Run on all problems:
    python3 probabilistic_maxsat_solver.py --run-all

Good luck and have fun! 🎲
"""

import os
import random
import math
import argparse
from util import Problem, write_assignment, evaluate_all, timeout, print_assignment_summary


# Paths
PROBLEMS_PATH = 'problems/'
RESULTS_PATH = 'results/'
REFERENCE_FILE = 'reference_results.txt'


def random_search_baseline(problem, iterations=1000):
    """
    A simple baseline: random search.
    Generates random assignments and keeps the best one.
    
    This is NOT what you should implement - it's just for comparison!
    
    Args:
        problem: A Problem instance
        iterations: Number of random samples to try
        
    Returns:
        Dictionary mapping predicates to values in [0,1]
    """
    predicates = list(problem.predicates())
    
    # Start with random assignment
    best_assignment = {pred: random.random() for pred in predicates}
    best_score = problem.evaluate(best_assignment)
    
    print(f"    Random search baseline: {iterations} iterations")
    
    for i in range(iterations):
        # Generate random assignment
        candidate = {pred: random.random() for pred in predicates}
        score = problem.evaluate(candidate)
        
        if score > best_score:
            best_score = score
            best_assignment = candidate
            print(f"      Iteration {i}: Found better solution with score {best_score:.2f}")
    
    print(f"    Final score: {best_score:.2f}")
    return best_assignment


# ============================================================================
# YOUR CODE GOES HERE!
# ============================================================================

@timeout(5 * 60)  # 5 minutes per problem
def hit_and_run(problem, iterations=10000, verbose=False):
    """
    Hit-and-Run algorithm for Probabilistic MaxSAT.
    
    The Hit-and-Run algorithm is a Markov Chain Monte Carlo (MCMC) method
    that samples points uniformly from a convex region (in our case, [0,1]^n).
    
    Algorithm:
    1. Start at a random point x in [0,1]^n
    2. Pick a random direction d (usually from unit sphere)
    3. Find the line segment L = {x + t*d : t ∈ [t_min, t_max]} that stays in [0,1]^n
    4. Sample a new point uniformly along L
    5. Repeat from the new point
    
    For optimization, we keep track of the best solution found.
    
    Args:
        problem: A Problem instance
        iterations: Number of iterations to run
        verbose: If True, print progress information
        
    Returns:
        Dictionary mapping predicates to values in [0,1]
    """
    predicates = list(problem.predicates())
    n = len(predicates)
    
    if verbose:
        print(f"    Hit-and-Run: {iterations} iterations on {n} variables")
    
    # TODO: Step 1 - Initialize with a random point in [0,1]^n
    current_assignment = None  # REPLACE THIS
    current_score = 0.0  # REPLACE THIS
    
    # Check if student implemented initialization
    if current_assignment is None:
        print("\n⚠️  WARNING: You need to implement the hit_and_run() function!")
        print("   Read INSTRUCTIONS.md for detailed guidance.")
        print("   Returning empty solution for now...\n")
        return {pred: 0.5 for pred in predicates}  # Return something valid
    
    # Keep track of the best solution found
    best_assignment = current_assignment
    best_score = current_score
    
    for iteration in range(iterations):
        # TODO: Step 2 - Pick a random direction
        direction = None  # REPLACE THIS
        
        # TODO: Step 3 - Find t_min and t_max
        # For each variable: 0 <= current[var] + t*direction[var] <= 1
        # This gives you bounds on t
        # You need to find the intersection of all these constraints
        t_min = None  # REPLACE THIS
        t_max = None  # REPLACE THIS
        
        # TODO: Step 4 - Sample t uniformly from [t_min, t_max]
        t = None  # REPLACE THIS
        
        # TODO: Step 5 - Compute new_assignment = current + t*direction
        new_assignment = None  # REPLACE THIS
        
        # TODO: Step 6 - Evaluate new assignment
        new_score = 0.0  # REPLACE THIS
        
        # TODO: Step 7 - Decide whether to move to new point
        # Basic Hit-and-Run
        # Or you can be smarter: only accept improvements, use simulated annealing, etc.
        
        # TODO: Step 8 - Update best if needed
        
        if verbose and iteration % 1000 == 0:
            print(f"      Iteration {iteration}: Best score so far {best_score:.2f}")
    
    if verbose:
        print(f"    Final best score: {best_score:.2f}")
    
    return best_assignment

def hit_and_run_with_restarts(problem, iterations=5000, num_restarts=3):
    """
    Run Hit-and-Run multiple times from different starting points
    and return the best solution found.
    
    This is a simple way to improve the algorithm!
    
    Args:
        problem: A Problem instance
        iterations: Number of iterations per restart
        num_restarts: Number of independent runs
        
    Returns:
        Dictionary mapping predicates to values in [0,1]
    """
    print(f"    Hit-and-Run with {num_restarts} restarts")
    
    best_assignment = None
    best_score = float('-inf')
    
    for restart in range(num_restarts):
        print(f"      Restart {restart + 1}/{num_restarts}")
        assignment = hit_and_run(problem, iterations=iterations // num_restarts, verbose=False)
        score = problem.evaluate(assignment)
        
        if score > best_score:
            best_score = score
            best_assignment = assignment
            print(f"        New best: {best_score:.2f}")
    
    print(f"    Final score: {best_score:.2f}")
    return best_assignment

# ============================================================================
# Test and Evaluation Functions
# ============================================================================

def example_hermione():
    """
    Run the solver on the Hermione example and display results.
    This is a good starting point for understanding the problem!
    """
    print("\n" + "="*70)
    print("🧙 HERMIONE EXAMPLE")
    print("="*70 + "\n")
    
    problem_file = os.path.join(PROBLEMS_PATH, 'hermione.txt')
    
    if not os.path.exists(problem_file):
        print("❌ Hermione problem file not found!")
        print(f"   Looking for: {problem_file}")
        return
    
    problem = Problem(problem_file)
    
    print("Problem clauses:")
    for i, clause in enumerate(problem.clauses, 1):
        print(f"  {i}. {clause}")
    
    print(f"\nVariables: {', '.join(sorted(problem.predicates()))}")
    print(f"Total possible weight: {problem.total_weight()}")
    
    print("\n" + "-"*70)
    print("Running Hit-and-Run solver...")
    print("-"*70 + "\n")
    
    # Run solver
    solution = hit_and_run(problem, iterations=5000, verbose=True)
    
    # Display solution
    print_assignment_summary(solution, problem)
    
    # Save result
    os.makedirs(RESULTS_PATH, exist_ok=True)
    result_file = os.path.join(RESULTS_PATH, 'hermione.res')
    write_assignment(solution, result_file)
    print(f"✅ Result saved to {result_file}")
    
    print("\n" + "="*70 + "\n")


def run_all_problems(solver_func=None):
    """
    Run the solver on all problems and evaluate results.
    
    Args:
        solver_func: The solver function to use (default: hit_and_run)
    """
    if solver_func is None:
        solver_func = hit_and_run
    
    if not os.path.exists(PROBLEMS_PATH):
        print(f"❌ Problems folder not found: {PROBLEMS_PATH}")
        return
    
    os.makedirs(RESULTS_PATH, exist_ok=True)
    
    print("\n" + "="*70)
    print("🚀 RUNNING SOLVER ON ALL PROBLEMS")
    print("="*70 + "\n")
    
    problem_files = sorted([f for f in os.listdir(PROBLEMS_PATH) if f.endswith('.txt')])
    
    for i, filename in enumerate(problem_files, 1):
        print(f"\n[{i}/{len(problem_files)}] Processing: {filename}")
        print("-"*70)
        
        problem_path = os.path.join(PROBLEMS_PATH, filename)
        result_path = os.path.join(RESULTS_PATH, filename.replace('.txt', '.res'))
        
        try:
            problem = Problem(problem_path)
            print(f"  Variables: {len(problem.predicates())}")
            print(f"  Clauses: {len(problem.clauses)}")
            print(f"  Max weight: {problem.total_weight():.2f}")
            
            # Solve
            solution = solver_func(problem)
            score = problem.evaluate(solution)
            percentage = (score / problem.total_weight() * 100) if problem.total_weight() > 0 else 0
            
            print(f"  ✅ Achieved: {score:.2f} ({percentage:.2f}%)")
            
            # Save
            write_assignment(solution, result_path)
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("📊 EVALUATION")
    print("="*70)
    
    # Evaluate all results
    evaluate_all(RESULTS_PATH, PROBLEMS_PATH, REFERENCE_FILE)


def compare_solvers():
    """
    Compare different solver strategies on a problem.
    """
    print("\n" + "="*70)
    print("🏆 SOLVER COMPARISON")
    print("="*70 + "\n")
    
    problem_file = os.path.join(PROBLEMS_PATH, 'hermione.txt')
    if not os.path.exists(problem_file):
        print("❌ Hermione problem file not found!")
        return
    
    problem = Problem(problem_file)
    
    solvers = [
        ("Random Search", lambda p: random_search_baseline(p, iterations=5000)),
        ("Hit-and-Run", lambda p: hit_and_run(p, iterations=5000, verbose=False)),
        ("Hit-and-Run + Restarts", lambda p: hit_and_run_with_restarts(p, iterations=5000, num_restarts=3)),
    ]
    
    results = []
    
    for name, solver_func in solvers:
        print(f"\n{name}:")
        print("-"*70)
        solution = solver_func(problem)
        score = problem.evaluate(solution)
        results.append((name, score, solution))
        print()
    
    print("\n" + "="*70)
    print("COMPARISON RESULTS")
    print("="*70 + "\n")
    
    for name, score, _ in sorted(results, key=lambda x: -x[1]):
        percentage = (score / problem.total_weight() * 100) if problem.total_weight() > 0 else 0
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"{name:25s} {score:7.2f} [{bar}] {percentage:.1f}%")
    
    print("\n" + "="*70 + "\n")


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Main entry point for the solver."""
    parser = argparse.ArgumentParser(description='Probabilistic MaxSAT Solver')
    parser.add_argument('--run-all', action='store_true', 
                       help='Run solver on all problems')
    parser.add_argument('--compare', action='store_true',
                       help='Compare different solvers')
    parser.add_argument('--baseline', action='store_true',
                       help='Use random search baseline instead of Hit-and-Run')
    
    args = parser.parse_args()
    
    if args.compare:
        compare_solvers()
    elif args.run_all:
        solver = random_search_baseline if args.baseline else hit_and_run
        run_all_problems(solver)
    else:
        # Default: run Hermione example
        example_hermione()


if __name__ == '__main__':
    main()
