# 🚀 Quick Start Guide

**Get started in 5 minutes!**

## ✅ Prerequisites

- Python 3.7 or higher
- No external libraries needed! (uses only Python standard library)

## 📦 What's in the Box?

```
ProbabilisticMaxSAT/
├── README.md                          # Overview and concepts
├── INSTRUCTIONS.md                    # Detailed lab instructions
├── QUICKSTART.md                      # This file!
├── probabilistic_maxsat_solver.py     # YOUR CODE GOES HERE
├── util.py                            # Helper functions (don't modify)
├── visualizer.py                      # Visualization tools
├── requirements.txt                   # Dependencies (none required!)
├── reference_results.txt              # Target scores
├── problems/                          # Test problems
│   ├── hermione.txt                   # Harry Potter example
│   ├── simple_2vars.txt               # 2-variable problem (for visualization)
│   ├── simple_3vars.txt               # 3-variable problem
│   ├── conflicting.txt                # Shows difference from binary logic
│   ├── implication.txt                # Rules with implications
│   └── ...                            # More benchmark problems
└── results/                           # Your results will be saved here
```

## 🏃 Running the Code

### 1. Test Basic Example

```bash
cd ProbabilisticMaxSAT
python3 probabilistic_maxsat_solver.py
```

This runs the Hit-and-Run algorithm on the Hermione problem. You should see:
- Problem description
- Progress messages
- Final solution with score
- Result saved to `results/hermione.res`

### 2. Run on All Problems

```bash
python3 probabilistic_maxsat_solver.py --run-all
```

This:
- Solves all problems in `problems/`
- Saves results to `results/`
- Compares your scores with reference results
- Shows summary statistics

### 3. Compare Different Strategies

```bash
python3 probabilistic_maxsat_solver.py --compare
```

This compares:
- Random search baseline
- Basic Hit-and-Run
- Hit-and-Run with restarts

### 4. Visualize a Solution

```bash
python3 visualizer.py problems/simple_2vars.txt results/simple_2vars.res
```

Shows:
- Variable values as bars
- Clause satisfaction degrees
- 2D heatmap (for 2-variable problems)

### 5. Watch the Algorithm in Action

```bash
python3 visualizer.py problems/hermione.txt --animate
```

Shows a step-by-step trace of the Hit-and-Run algorithm!

## 📝 Your Task

**Open `probabilistic_maxsat_solver.py` and implement the `hit_and_run()` function.**

The starter code already has a working implementation - your job is to:
1. **Understand it**: Read the code and comments carefully
2. **Improve it**: Try different strategies (optional but fun!)
3. **Test it**: Make sure it works on all problems

### Where is the Code?

Look for this in `probabilistic_maxsat_solver.py`:

```python
@timeout(5 * 60)  # 5 minutes per problem
def hit_and_run(problem, iterations=10000, verbose=False):
    """
    Hit-and-Run algorithm for Probabilistic MaxSAT.
    
    YOUR CODE GOES HERE!
    """
    # ... implementation ...
```

## 🎯 Success Criteria

Your implementation should:
- ✅ Run without errors on all problems
- ✅ Keep variables in [0, 1] range
- ✅ Achieve at least 80% of reference scores
- ✅ Complete within time limit (5 minutes per problem)

## 💡 Tips for Success

### 1. Start Simple
```bash
# Test on the smallest problem first
python3 probabilistic_maxsat_solver.py
```

### 2. Use Visualization
```bash
# Understand the problem visually
python3 visualizer.py problems/simple_2vars.txt --animate
```

### 3. Debug with Print Statements
```python
def hit_and_run(problem, iterations=10000, verbose=True):
    # ... your code ...
    if verbose and iteration % 1000 == 0:
        print(f"Iteration {iteration}: score = {current_score:.2f}")
```

### 4. Check Correctness
```bash
# Make sure your solution is valid
python3 -c "
from util import Problem, load_assignment
p = Problem('problems/hermione.txt')
a = load_assignment('results/hermione.res')
print('All values in [0,1]:', all(0 <= v <= 1 for v in a.values()))
print('Score:', p.evaluate(a))
"
```

## 🐛 Troubleshooting

### Error: "File not found"
```bash
# Make sure you're in the right directory
cd ProbabilisticMaxSAT
pwd  # Should end with /ProbabilisticMaxSAT
```

### Error: "Division by zero"
```python
# Check for zero direction components
if abs(dir_val) < 1e-10:
    continue
```

### Error: "Value out of range"
```python
# Always clamp values to [0,1]
value = max(0.0, min(1.0, value))
```

### Issue: "Too slow"
```python
# Reduce iterations for testing
solution = hit_and_run(problem, iterations=1000)
```

### Issue: "Bad scores"
```bash
# Compare with baseline
python3 probabilistic_maxsat_solver.py --compare
```

## 📚 Next Steps

1. ✅ **Understand the basics** - Read README.md
2. ✅ **Run the examples** - Follow this quickstart
3. ✅ **Read the instructions** - Check INSTRUCTIONS.md
4. ✅ **Implement your solution** - Edit probabilistic_maxsat_solver.py
5. ✅ **Test thoroughly** - Try all problems
6. ✅ **Experiment** (optional) - Try improvements!

## 🎮 Fun Challenges (Optional)

Once you have a working solution, try these:

### Challenge 1: Beat the Reference
Can you achieve better scores than `reference_results.txt`?

### Challenge 2: Speed Record
How few iterations can you use and still get good results?

### Challenge 3: New Strategies
Implement:
- Simulated annealing
- Adaptive step sizes
- Smart initialization
- Multiple restarts

### Challenge 4: Create Your Own Problems
Make interesting problems and test your solver on them!

### Challenge 5: Visualize Your Strategy
Modify `visualizer.py` to show your algorithm's behavior.

## ❓ Questions?

- **Not sure how Hit-and-Run works?** → Read INSTRUCTIONS.md section "The Hit-and-Run Algorithm"
- **Don't understand Łukasiewicz logic?** → Read README.md section "How Clauses Work"
- **Code not working?** → Try the simplest example first: `problems/simple_2vars.txt`
- **Want to go deeper?** → Check the resources in INSTRUCTIONS.md

## 🎉 Ready to Start?

```bash
# 1. Go to the directory
cd ProbabilisticMaxSAT

# 2. Run the basic example
python3 probabilistic_maxsat_solver.py

# 3. Open the solver in your editor
# YOUR FAVORITE EDITOR probabilistic_maxsat_solver.py

# 4. Have fun! 🚀
```

---

**Remember**: This is a **non-graded** lab about learning and exploration. Focus on understanding the concepts, not on perfect scores. Enjoy the journey! 🎓

