"""
Interactive Exploration Notebook for Probabilistic MaxSAT

This is a Python script that can be run interactively in a Jupyter notebook
or step-by-step in a Python REPL.

To use in Jupyter:
    jupyter notebook exploration_notebook.ipynb

To use in Python REPL:
    python3 -i exploration_notebook.py
"""

# %% Imports and Setup
import random
import math
from util import Problem, Atom, Clause, print_assignment_summary, compare_assignments
from probabilistic_maxsat_solver import hit_and_run, random_search_baseline

# %% Cell 1: Understanding Atoms and Truth Values

print("="*70)
print("CELL 1: Understanding Atoms in Probabilistic Logic")
print("="*70 + "\n")

# Create a positive atom
atom_pos = Atom("harryIsSmart", polarity=True)
print(f"Positive atom: {atom_pos}")

# Create a negative atom
atom_neg = Atom("-hermioneIsLazy", polarity=True)
print(f"Negative atom: {atom_neg}")

# Test truth values
assignment = {
    "harryIsSmart": 0.7,
    "hermioneIsLazy": 0.2
}

print(f"\nAssignment: {assignment}")
print(f"Truth value of {atom_pos}: {atom_pos.truth_value(assignment)}")
print(f"Truth value of {atom_neg}: {atom_neg.truth_value(assignment)}")

# Key insight: negation in Łukasiewicz logic
print("\n💡 Key Insight:")
print("In Łukasiewicz logic, ¬A = 1 - A")
print(f"If harryIsSmart = 0.7, then -harryIsSmart = {1 - 0.7}")

# %% Cell 2: Understanding Clauses and Satisfaction

print("\n" + "="*70)
print("CELL 2: Understanding Clause Satisfaction")
print("="*70 + "\n")

# Create a clause
clause = Clause("{harryIsSmart, hermioneIsSmart} [10]")
print(f"Clause: {clause}")

# Test different assignments
test_cases = [
    {"harryIsSmart": 1.0, "hermioneIsSmart": 0.0},
    {"harryIsSmart": 0.5, "hermioneIsSmart": 0.5},
    {"harryIsSmart": 0.7, "hermioneIsSmart": 0.3},
    {"harryIsSmart": 0.0, "hermioneIsSmart": 0.0},
]

print("\nTesting different assignments:")
print("-"*70)
for i, assignment in enumerate(test_cases, 1):
    degree = clause.satisfaction_degree(assignment)
    weighted = clause.weighted_satisfaction(assignment)
    print(f"\nCase {i}: {assignment}")
    print(f"  Satisfaction degree: {degree:.2f}")
    print(f"  Weighted satisfaction: {weighted:.2f}")

print("\n💡 Key Insight:")
print("Łukasiewicz disjunction: A ∨ B = min(1, A + B)")
print("The clause is fully satisfied when the sum of truth values ≥ 1")

# %% Cell 3: The Conflicting Clauses Problem

print("\n" + "="*70)
print("CELL 3: Conflicting Clauses - Why Probabilistic Logic Helps")
print("="*70 + "\n")

# Create conflicting clauses
clause_A = Clause("{A} [10]")
clause_notA = Clause("{-A} [10]")

print("In classical logic:")
print(f"  {clause_A}")
print(f"  {clause_notA}")
print("  → Can only satisfy one! Max weight = 10\n")

print("In probabilistic logic:")
test_values = [0.0, 0.25, 0.5, 0.75, 1.0]

for val in test_values:
    assignment = {"A": val}
    w1 = clause_A.weighted_satisfaction(assignment)
    w2 = clause_notA.weighted_satisfaction(assignment)
    total = w1 + w2
    print(f"  A = {val:.2f}: w1 = {w1:5.2f}, w2 = {w2:5.2f}, total = {total:5.2f}")

print("\n💡 Key Insight:")
print("With A = 0.5, both clauses get 0.5 satisfaction!")
print("Total weight = 10.0 (vs. 10.0 in classical logic)")
print("Probabilistic logic helps balance conflicting constraints!")

# %% Cell 4: Load and Explore the Hermione Problem

print("\n" + "="*70)
print("CELL 4: The Hermione Problem")
print("="*70 + "\n")

problem = Problem("problems/hermione.txt")

print(f"Problem: {problem}")
print(f"Variables: {', '.join(sorted(problem.predicates()))}")
print(f"Total weight: {problem.total_weight()}\n")

print("Clauses:")
for i, clause in enumerate(problem.clauses, 1):
    print(f"  {i}. {clause}")

# %% Cell 5: Compare Different Assignments

print("\n" + "="*70)
print("CELL 5: Comparing Different Assignments")
print("="*70 + "\n")

# Assignment 1: All variables = 0.5
assignment1 = {pred: 0.5 for pred in problem.predicates()}
score1 = problem.evaluate(assignment1)

# Assignment 2: Random
assignment2 = {pred: random.random() for pred in problem.predicates()}
score2 = problem.evaluate(assignment2)

# Assignment 3: Based on intuition
assignment3 = {
    "harryIsSmart": 1.0,
    "hermioneIsSmart": 1.0,
    "likesHermioneHarry": 0.0,
    "likesHermioneRon": 1.0
}
score3 = problem.evaluate(assignment3)

print("Assignment 1 (all 0.5):")
print(f"  Score: {score1:.2f}")

print("\nAssignment 2 (random):")
print(f"  Score: {score2:.2f}")

print("\nAssignment 3 (intuitive):")
print(f"  Score: {score3:.2f}")

# %% Cell 6: Visualize Hit-and-Run Steps

print("\n" + "="*70)
print("CELL 6: Hit-and-Run Algorithm Steps")
print("="*70 + "\n")

# Manual Hit-and-Run steps
predicates = list(problem.predicates())
current = {pred: random.random() for pred in predicates}

print("Starting point:")
print(f"  {current}")
print(f"  Score: {problem.evaluate(current):.2f}\n")

print("Performing 5 Hit-and-Run steps:\n")

for step in range(5):
    # Pick random direction
    direction = {pred: random.gauss(0, 1) for pred in predicates}
    length = math.sqrt(sum(d*d for d in direction.values()))
    direction = {pred: d/length for pred, d in direction.items()}
    
    # Find valid t range
    t_min = float('-inf')
    t_max = float('inf')
    
    for pred in predicates:
        current_val = current[pred]
        dir_val = direction[pred]
        
        if abs(dir_val) < 1e-10:
            continue
        
        t1 = -current_val / dir_val
        t2 = (1 - current_val) / dir_val
        
        if t1 > t2:
            t1, t2 = t2, t1
        
        t_min = max(t_min, t1)
        t_max = min(t_max, t2)
    
    # Sample t
    if t_min < t_max:
        t = random.uniform(t_min, t_max)
        new = {pred: max(0.0, min(1.0, current[pred] + t * direction[pred])) 
               for pred in predicates}
        new_score = problem.evaluate(new)
        
        print(f"Step {step + 1}:")
        print(f"  Sampled t = {t:.3f} from range [{t_min:.3f}, {t_max:.3f}]")
        print(f"  New position: {new}")
        print(f"  New score: {new_score:.2f}\n")
        
        current = new

# %% Cell 7: Run and Compare Solvers

print("\n" + "="*70)
print("CELL 7: Running Different Solvers")
print("="*70 + "\n")

# Random search
print("Running Random Search (1000 iterations)...")
sol_random = random_search_baseline(problem, iterations=1000)
score_random = problem.evaluate(sol_random)
print()

# Basic Hit-and-Run
print("Running Hit-and-Run (5000 iterations)...")
sol_hitrun = hit_and_run(problem, iterations=5000, verbose=False)
score_hitrun = problem.evaluate(sol_hitrun)
print(f"  Final score: {score_hitrun:.2f}\n")

# Compare
print("Comparison:")
print(f"  Random Search: {score_random:.2f} / {problem.total_weight():.2f} ({score_random/problem.total_weight()*100:.1f}%)")
print(f"  Hit-and-Run:   {score_hitrun:.2f} / {problem.total_weight():.2f} ({score_hitrun/problem.total_weight()*100:.1f}%)")

# %% Cell 8: Detailed Analysis of Best Solution

print("\n" + "="*70)
print("CELL 8: Detailed Analysis of Best Solution")
print("="*70 + "\n")

best = sol_hitrun
print_assignment_summary(best, problem)

# Detailed clause-by-clause analysis
print("\n" + "="*70)
print("Clause-by-Clause Analysis")
print("="*70 + "\n")

results = problem.detailed_evaluation(best)
for i, clause_result in enumerate(results['by_clause'], 1):
    print(f"Clause {i}: {clause_result['clause']}")
    print(f"  Satisfaction degree: {clause_result['degree']:.3f}")
    print(f"  Weight: {clause_result['weight']:.1f}")
    print(f"  Contribution: {clause_result['weighted_satisfaction']:.2f}")
    print()

print(f"Total: {results['total']:.2f} / {results['max_possible']:.2f} ({results['percentage']:.2f}%)")

# %% Cell 9: Experiment with Different Parameters

print("\n" + "="*70)
print("CELL 9: Parameter Experiments")
print("="*70 + "\n")

# Test different iteration counts
iteration_counts = [100, 500, 1000, 5000, 10000]

print("Testing different iteration counts:\n")
for iters in iteration_counts:
    solution = hit_and_run(problem, iterations=iters, verbose=False)
    score = problem.evaluate(solution)
    percentage = (score / problem.total_weight() * 100)
    print(f"  {iters:5d} iterations: {score:6.2f} ({percentage:5.2f}%)")

# %% Cell 10: Create Your Own Problem!

print("\n" + "="*70)
print("CELL 10: Create Your Own Problem")
print("="*70 + "\n")

print("Try creating your own problem!")
print("\nExample:")
print("  clause1 = Clause('{X, Y} [10]')")
print("  clause2 = Clause('{-X, Z} [5]')")
print("  ... then solve it!\n")

# Example custom problem
custom_clauses_text = [
    "{sunny, happy} [10]",
    "{-rainy, happy} [8]",
    "{rainy, -sunny} [5]",
    "=> sunny [3]"
]

print("Example custom problem:")
for clause_text in custom_clauses_text:
    print(f"  {clause_text}")

# %% Summary

print("\n" + "="*70)
print("🎉 EXPLORATION COMPLETE!")
print("="*70 + "\n")

print("What you've learned:")
print("  ✅ How probabilistic atoms have continuous truth values [0,1]")
print("  ✅ How Łukasiewicz logic computes clause satisfaction")
print("  ✅ Why probabilistic logic helps with conflicting constraints")
print("  ✅ How Hit-and-Run explores the solution space")
print("  ✅ How to analyze and compare different solutions")

print("\nNext steps:")
print("  1. Implement improvements to hit_and_run()")
print("  2. Test on larger problems")
print("  3. Visualize solutions with visualizer.py")
print("  4. Create your own interesting problems!")

print("\n" + "="*70 + "\n")

# %% Instructions for Interactive Use

"""
To use this file interactively:

Option 1: Jupyter Notebook (if you have it)
    1. Convert to notebook: jupyter nbconvert --to notebook exploration_notebook.py
    2. Open: jupyter notebook exploration_notebook.ipynb

Option 2: IPython
    1. Run: ipython -i exploration_notebook.py
    2. Experiment with variables and functions

Option 3: Python REPL
    1. Run: python3 -i exploration_notebook.py
    2. Access all defined variables and functions

Option 4: Run as script
    1. Run: python3 exploration_notebook.py
    2. See all output at once
"""

