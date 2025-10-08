"""
Visualizer for Probabilistic MaxSAT Solutions

This module provides interactive visualizations for understanding
how Hit-and-Run explores the solution space.

Usage:
    python visualizer.py problems/hermione.txt results/hermione.res
"""

import sys
import os
from util import Problem, load_assignment
import random
import math


def visualize_2d_problem(problem, assignment=None, num_samples=50):
    """
    Create an ASCII art visualization for problems with 2 variables.
    Shows the objective function landscape and the solution point.
    
    Args:
        problem: Problem instance (must have exactly 2 variables)
        assignment: Optional assignment to highlight
        num_samples: Resolution of the heatmap
    """
    predicates = sorted(problem.predicates())
    
    if len(predicates) != 2:
        print(f"Cannot visualize: problem has {len(predicates)} variables (need exactly 2)")
        return
    
    var1, var2 = predicates
    max_weight = problem.total_weight()
    
    print("\n" + "="*70)
    print(f"📊 2D VISUALIZATION: {var1} vs {var2}")
    print("="*70 + "\n")
    
    # Create heatmap
    print("Objective function landscape (higher values are better):")
    print(f"\n{var2:>10s} ↑")
    
    for i in range(num_samples, -1, -1):
        val2 = i / num_samples
        line = f"{val2:4.1f} │ "
        
        for j in range(num_samples + 1):
            val1 = j / num_samples
            
            test_assignment = {var1: val1, var2: val2}
            score = problem.evaluate(test_assignment)
            percentage = (score / max_weight) if max_weight > 0 else 0
            
            # Check if this is the solution point
            is_solution = False
            if assignment:
                if abs(assignment.get(var1, 0) - val1) < 0.05 and \
                   abs(assignment.get(var2, 0) - val2) < 0.05:
                    is_solution = True
            
            if is_solution:
                line += "🎯"
            elif percentage > 0.9:
                line += "██"
            elif percentage > 0.7:
                line += "▓▓"
            elif percentage > 0.5:
                line += "▒▒"
            elif percentage > 0.3:
                line += "░░"
            else:
                line += "  "
        
        print(line)
    
    print(f"     └" + "─"*(num_samples*2) + f"→ {var1}")
    print(f"      0.0" + " "*(num_samples*2-7) + "1.0")
    
    print("\nLegend:")
    print("  ██ = 90-100%  ▓▓ = 70-90%  ▒▒ = 50-70%  ░░ = 30-50%  __ = 0-30%")
    print("  🎯 = Your solution")
    
    if assignment:
        print(f"\nYour solution:")
        print(f"  {var1} = {assignment.get(var1, 0):.3f}")
        print(f"  {var2} = {assignment.get(var2, 0):.3f}")
        score = problem.evaluate(assignment)
        print(f"  Score = {score:.2f} / {max_weight:.2f} ({score/max_weight*100:.1f}%)")
    
    print("\n" + "="*70 + "\n")


def visualize_assignment_bars(problem, assignment):
    """
    Show assignment values as horizontal bars.
    
    Args:
        problem: Problem instance
        assignment: Assignment to visualize
    """
    print("\n" + "="*70)
    print("📊 VARIABLE VALUES")
    print("="*70 + "\n")
    
    predicates = sorted(assignment.keys())
    
    for pred in predicates:
        value = assignment[pred]
        bar_length = int(value * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        print(f"{pred:30s} │{bar}│ {value:.3f}")
    
    print("\n" + "="*70)
    print("📋 CLAUSE SATISFACTION")
    print("="*70 + "\n")
    
    total = 0.0
    for i, clause in enumerate(problem.clauses, 1):
        degree = clause.satisfaction_degree(assignment)
        weighted = clause.weighted_satisfaction(assignment)
        total += weighted
        
        bar_length = int(degree * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        
        print(f"Clause {i:2d}: │{bar}│ {degree:.2f} × {clause.weight:6.1f} = {weighted:7.2f}")
        print(f"           {clause}")
    
    max_weight = problem.total_weight()
    percentage = (total / max_weight * 100) if max_weight > 0 else 0
    
    print("\n" + "="*70)
    print(f"TOTAL: {total:.2f} / {max_weight:.2f} ({percentage:.2f}%)")
    print("="*70 + "\n")


def animate_hit_and_run(problem, iterations=20):
    """
    Show an animated trace of Hit-and-Run algorithm (works best with 2-3 variables).
    
    Args:
        problem: Problem instance
        iterations: Number of iterations to show
    """
    predicates = list(problem.predicates())
    n = len(predicates)
    
    print("\n" + "="*70)
    print("🎬 HIT-AND-RUN ANIMATION")
    print("="*70 + "\n")
    
    # Initialize
    current = {pred: random.random() for pred in predicates}
    current_score = problem.evaluate(current)
    
    best = current.copy()
    best_score = current_score
    
    print(f"Starting at: {current}")
    print(f"Initial score: {current_score:.2f}")
    print("\n" + "-"*70 + "\n")
    
    for iteration in range(iterations):
        print(f"Iteration {iteration + 1}:")
        
        # Pick random direction
        direction = {pred: random.gauss(0, 1) for pred in predicates}
        length = math.sqrt(sum(d*d for d in direction.values()))
        if length > 0:
            direction = {pred: d/length for pred, d in direction.items()}
        
        print(f"  Direction: {direction}")
        
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
        
        print(f"  Valid t range: [{t_min:.3f}, {t_max:.3f}]")
        
        # Sample t
        if t_min < t_max:
            t = random.uniform(t_min, t_max)
            print(f"  Sampled t = {t:.3f}")
            
            # Create new assignment
            new = {
                pred: max(0.0, min(1.0, current[pred] + t * direction[pred]))
                for pred in predicates
            }
            
            new_score = problem.evaluate(new)
            
            print(f"  New point: {new}")
            print(f"  New score: {new_score:.2f}")
            
            # Update
            current = new
            current_score = new_score
            
            if new_score > best_score:
                best = new.copy()
                best_score = new_score
                print(f"  🎉 New best!")
        else:
            print(f"  ⚠️ No valid range!")
        
        print()
    
    print("="*70)
    print("FINAL RESULTS")
    print("="*70)
    print(f"Best score: {best_score:.2f}")
    print(f"Best assignment: {best}")
    print("="*70 + "\n")


def main():
    """Main entry point for visualizer."""
    if len(sys.argv) < 2:
        print("Usage: python visualizer.py <problem_file> [result_file]")
        print("\nExamples:")
        print("  python visualizer.py problems/hermione.txt")
        print("  python visualizer.py problems/hermione.txt results/hermione.res")
        print("  python visualizer.py problems/hermione.txt --animate")
        return
    
    problem_file = sys.argv[1]
    
    if not os.path.exists(problem_file):
        print(f"❌ Problem file not found: {problem_file}")
        return
    
    problem = Problem(problem_file)
    print(f"\n✅ Loaded problem: {problem}")
    
    # Check for animation flag
    if len(sys.argv) > 2 and sys.argv[2] == '--animate':
        animate_hit_and_run(problem, iterations=10)
        return
    
    # Load result if provided
    assignment = None
    if len(sys.argv) > 2:
        result_file = sys.argv[2]
        if os.path.exists(result_file):
            assignment = load_assignment(result_file)
            print(f"✅ Loaded assignment from: {result_file}")
        else:
            print(f"⚠️ Result file not found: {result_file}")
            print("Creating random assignment for demonstration...")
            assignment = {pred: random.random() for pred in problem.predicates()}
    else:
        print("No result file provided, creating random assignment...")
        assignment = {pred: random.random() for pred in problem.predicates()}
    
    # Visualize
    visualize_assignment_bars(problem, assignment)
    
    # Try 2D visualization if possible
    if len(problem.predicates()) == 2:
        visualize_2d_problem(problem, assignment, num_samples=30)
    elif len(problem.predicates()) < 2:
        print("⚠️ Problem has less than 2 variables, cannot create 2D visualization")
    else:
        print(f"⚠️ Problem has {len(problem.predicates())} variables")
        print("   2D visualization only works with exactly 2 variables")
        print("   Try with: problems/simple_2vars.txt")


if __name__ == '__main__':
    main()

