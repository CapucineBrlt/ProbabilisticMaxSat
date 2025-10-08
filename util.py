"""
Utility classes and functions for Probabilistic MaxSAT

This module provides the core data structures for working with
probabilistic logic formulas and clauses.

DO NOT MODIFY THIS FILE (unless you want to experiment with different logics!)
"""

import re
import os
from threading import Thread
import functools


class Atom:
    """
    A logical atom in probabilistic logic.
    Unlike classical logic, atoms have continuous truth values in [0,1].
    """
    
    def __init__(self, atom_text, polarity=True):
        """
        Creates an atom from text like 'harryIsSmart' or '-hermioneIsLazy'
        
        Args:
            atom_text: String representation of the atom
            polarity: Whether the atom is positive (True) or negated (False)
        """
        self.predicate = None
        self.polarity = None
        
        atom_text = atom_text.strip()
        if not re.match('-?[a-zA-Z_0-9]+', atom_text):
            raise Exception(f'Malformed atom: {atom_text}')
            
        if atom_text.startswith('-'):
            self.predicate = atom_text[1:]
            self.polarity = not polarity
        else:
            self.predicate = atom_text
            self.polarity = polarity
    
    def is_positive(self):
        return self.polarity
    
    def is_negative(self):
        return not self.polarity
    
    def flip_polarity(self):
        """Returns a new atom with opposite polarity"""
        return Atom(self.predicate, not self.polarity)
    
    def truth_value(self, assignment):
        """
        Get the truth value of this atom given a probabilistic assignment.
        
        Args:
            assignment: Dictionary mapping predicates to values in [0,1]
            
        Returns:
            Truth value in [0,1]
        """
        base_value = assignment.get(self.predicate, 0.0)
        if self.is_positive():
            return base_value
        else:
            # Negation in Łukasiewicz logic: ¬A = 1 - A
            return 1.0 - base_value
    
    def __str__(self):
        return ("" if self.polarity else '-') + self.predicate
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return self.predicate == other.predicate and self.polarity == other.polarity
    
    def __hash__(self):
        return hash(self.predicate)


class Clause:
    """
    A clause in probabilistic logic.
    Uses Łukasiewicz logic for computing satisfaction degree.
    """
    
    def __init__(self, rule):
        """
        Creates a clause from a string like:
        - 'A & B => C [weight]'  (implication rule)
        - '{A, B, C} [weight]'   (disjunction)
        - 'A [weight]'           (single atom)
        
        Args:
            rule: String representation of the clause
        """
        self.atoms = []
        self.weight = 0.0
        
        # Extract weight from the end
        match_obj = re.search(r'\[?(\d+(\.\d*)?)\]?\s*$', rule)
        if not match_obj:
            raise Exception(f'Clause does not have a weight: {rule}')
        self.weight = float(match_obj.group(1))
        rule = rule[:match_obj.span()[0]].strip()
        
        # Parse rule format: A & B => C
        if '=>' in rule:
            parts = rule.split('=>')
            if len(parts) != 2:
                raise Exception(f"Rule must contain exactly one '=>': {rule}")
            
            # Body atoms become negated (A & B => C becomes ¬A ∨ ¬B ∨ C)
            for atom_text in parts[0].split('&'):
                atom_text = atom_text.strip()
                if atom_text:
                    self.atoms.append(Atom(atom_text).flip_polarity())
            
            # Head atom stays positive
            self.atoms.append(Atom(parts[1].strip()))
            return
        
        # Parse set format: {A, B, C}
        if rule.startswith('{') and rule.endswith('}'):
            rule = rule[1:-1]
        
        for atom_text in rule.split(','):
            atom_text = atom_text.strip()
            if atom_text:
                self.atoms.append(Atom(atom_text))
    
    def satisfaction_degree(self, assignment):
        """
        Compute how satisfied this clause is under a probabilistic assignment.
        Uses Łukasiewicz t-conorm for disjunction: min(1, sum of truth values)
        
        Args:
            assignment: Dictionary mapping predicates to values in [0,1]
            
        Returns:
            Satisfaction degree in [0,1]
        """
        # Łukasiewicz disjunction: A ∨ B = min(1, A + B)
        total = sum(atom.truth_value(assignment) for atom in self.atoms)
        return min(1.0, total)
    
    def weighted_satisfaction(self, assignment):
        """
        Compute the weighted satisfaction: degree × weight
        
        Args:
            assignment: Dictionary mapping predicates to values in [0,1]
            
        Returns:
            Weighted satisfaction value
        """
        return self.satisfaction_degree(assignment) * self.weight
    
    def __str__(self):
        atoms_str = ', '.join(str(atom) for atom in self.atoms)
        return f'{{{atoms_str}}} [{self.weight}]'
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return self.atoms == other.atoms and self.weight == other.weight
    
    def __hash__(self):
        return hash(tuple(self.atoms))


class Problem:
    """
    A Probabilistic MaxSAT problem: a set of weighted clauses.
    Goal: Find assignment maximizing sum of weighted satisfactions.
    """
    
    def __init__(self, file_path):
        """
        Load a problem from a file.
        
        Args:
            file_path: Path to problem file
        """
        self.clauses = []
        self.file_path = file_path
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.clauses.append(Clause(line))
    
    def predicates(self):
        """Get set of all predicates (variable names) in the problem"""
        return set(atom.predicate for clause in self.clauses for atom in clause.atoms)
    
    def evaluate(self, assignment):
        """
        Evaluate total weighted satisfaction for an assignment.
        
        Args:
            assignment: Dictionary mapping predicates to values in [0,1]
            
        Returns:
            Total weight of satisfied clauses
        """
        return sum(clause.weighted_satisfaction(assignment) for clause in self.clauses)
    
    def total_weight(self):
        """Get sum of all clause weights (theoretical maximum)"""
        return sum(clause.weight for clause in self.clauses)
    
    def detailed_evaluation(self, assignment):
        """
        Evaluate assignment and return detailed information.
        
        Args:
            assignment: Dictionary mapping predicates to values in [0,1]
            
        Returns:
            Dictionary with evaluation details
        """
        results = {
            'total': 0.0,
            'by_clause': [],
            'max_possible': self.total_weight()
        }
        
        for clause in self.clauses:
            degree = clause.satisfaction_degree(assignment)
            weighted = clause.weighted_satisfaction(assignment)
            results['by_clause'].append({
                'clause': str(clause),
                'degree': degree,
                'weight': clause.weight,
                'weighted_satisfaction': weighted
            })
            results['total'] += weighted
        
        results['percentage'] = (results['total'] / results['max_possible'] * 100) if results['max_possible'] > 0 else 0
        return results
    
    def __str__(self):
        return f"Problem with {len(self.clauses)} clauses, {len(self.predicates())} variables"
    
    def __repr__(self):
        return str(self)


def load_assignment(file_path):
    """
    Load a probabilistic assignment from a file.
    Format: one line per variable: 'predicate value'
    
    Args:
        file_path: Path to assignment file
        
    Returns:
        Dictionary mapping predicates to values in [0,1]
    """
    assignment = {}
    if not os.path.exists(file_path):
        return assignment
        
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 2:
                    predicate = parts[0]
                    value = float(parts[1])
                    # Ensure value is in [0,1]
                    assignment[predicate] = max(0.0, min(1.0, value))
    
    return assignment


def write_assignment(assignment, file_path):
    """
    Write a probabilistic assignment to a file.
    
    Args:
        assignment: Dictionary mapping predicates to values in [0,1]
        file_path: Path to output file
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("# Probabilistic Assignment\n")
        f.write("# Format: predicate value\n")
        f.write("#\n")
        for predicate in sorted(assignment.keys()):
            value = assignment[predicate]
            f.write(f"{predicate} {value:.6f}\n")


def evaluate_all(results_folder, problems_folder, reference_file=None):
    """
    Evaluate all results and compare with reference if provided.
    
    Args:
        results_folder: Folder containing result files
        problems_folder: Folder containing problem files
        reference_file: Optional file with reference results
        
    Returns:
        Average score across all problems
    """
    reference_results = {}
    if reference_file and os.path.isfile(reference_file):
        with open(reference_file, 'r', encoding='utf-8') as f:
            text = f.read()
            for match in re.finditer(r'(.+\.txt)\s*:\s*Weight\s*:\s*([0-9.]+)', text):
                reference_results[match.group(1)] = float(match.group(2))
    
    total_score = 0.0
    num_problems = 0
    reference_score = 0.0
    
    print("\n" + "="*70)
    print("EVALUATION RESULTS")
    print("="*70)
    
    for filename in sorted(os.listdir(problems_folder)):
        if not filename.endswith('.txt'):
            continue
            
        problem_path = os.path.join(problems_folder, filename)
        result_path = os.path.join(results_folder, filename.replace('.txt', '.res'))
        
        problem = Problem(problem_path)
        max_weight = problem.total_weight()
        
        print(f"\n📄 {filename}")
        print(f"   Max possible weight: {max_weight:.2f}")
        
        if not os.path.exists(result_path):
            print("   ❌ No result file found")
            continue
        
        assignment = load_assignment(result_path)
        achieved_weight = problem.evaluate(assignment)
        score = (achieved_weight / max_weight * 100) if max_weight > 0 else 0
        
        print(f"   Achieved weight: {achieved_weight:.2f}")
        print(f"   Score: {score:.2f}%")
        
        if filename in reference_results:
            ref_weight = reference_results[filename]
            ref_ratio = (achieved_weight / ref_weight * 100) if ref_weight > 0 else 0
            print(f"   Reference weight: {ref_weight:.2f}")
            print(f"   vs Reference: {ref_ratio:.2f}%")
            reference_score += ref_ratio
        
        total_score += score
        num_problems += 1
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Problems evaluated: {num_problems}")
    
    if num_problems > 0:
        avg_score = total_score / num_problems
        print(f"Average score: {avg_score:.2f}%")
        
        if reference_score > 0:
            avg_ref = reference_score / num_problems
            print(f"Average vs reference: {avg_ref:.2f}%")
    
    print("="*70 + "\n")
    
    return total_score / num_problems if num_problems > 0 else 0


def timeout(seconds):
    """
    Timeout decorator - stops function if it runs too long.
    
    Args:
        seconds: Maximum allowed execution time
        
    Returns:
        Decorated function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = [Exception(f'Function [{func.__name__}] timeout [{seconds} seconds] exceeded!')]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    result[0] = e
            
            thread = Thread(target=target)
            thread.daemon = True
            
            try:
                thread.start()
                thread.join(seconds)
            except Exception as e:
                print(f'Error starting thread: {e}')
                raise e
            
            ret = result[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        
        return wrapper
    return decorator


# Fun helper functions for visualization and debugging

def print_assignment_summary(assignment, problem=None):
    """
    Pretty-print an assignment and its evaluation.
    
    Args:
        assignment: Dictionary mapping predicates to values
        problem: Optional Problem to evaluate against
    """
    print("\n" + "🎯 ASSIGNMENT SUMMARY " + "="*50)
    
    for predicate in sorted(assignment.keys()):
        value = assignment[predicate]
        bar_length = int(value * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"{predicate:30s} [{bar}] {value:.3f}")
    
    if problem:
        total = problem.evaluate(assignment)
        max_possible = problem.total_weight()
        percentage = (total / max_possible * 100) if max_possible > 0 else 0
        print(f"\n{'='*70}")
        print(f"Total Weight: {total:.2f} / {max_possible:.2f} ({percentage:.2f}%)")
        print(f"{'='*70}\n")


def compare_assignments(assignment1, assignment2, labels=("Assignment 1", "Assignment 2")):
    """
    Compare two assignments side by side.
    
    Args:
        assignment1, assignment2: Assignments to compare
        labels: Names for the assignments
    """
    all_predicates = sorted(set(assignment1.keys()) | set(assignment2.keys()))
    
    print("\n" + "🔍 ASSIGNMENT COMPARISON " + "="*45)
    print(f"{'Variable':30s} {labels[0]:>15s} {labels[1]:>15s} {'Diff':>10s}")
    print("="*75)
    
    for predicate in all_predicates:
        val1 = assignment1.get(predicate, 0.0)
        val2 = assignment2.get(predicate, 0.0)
        diff = val2 - val1
        diff_str = f"{diff:+.3f}"
        print(f"{predicate:30s} {val1:>15.3f} {val2:>15.3f} {diff_str:>10s}")
    
    print("="*75 + "\n")

