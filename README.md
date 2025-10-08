# 🎲 Probabilistic MaxSAT - Hit-and-Run Algorithm

Welcome to the **Probabilistic MaxSAT** lab! This is a fun and interactive exploration of fuzzy logic and probabilistic reasoning.

## 🚀 Quick Start - Your Task

**Implement the Hit-and-Run algorithm** in `probabilistic_maxsat_solver.py`.

### Getting Started in 3 Steps:

1. **Run the example** (it will show a warning - that's expected!):
   ```bash
   python3 probabilistic_maxsat_solver.py
   ```

2. **Read this README** to understand the concepts below

3. **Implement `hit_and_run()`** in `probabilistic_maxsat_solver.py`:
   - Follow the TODOs and hints in the code
   - See `INSTRUCTIONS.md` for detailed guidance
   - Use `exploration_notebook.py` for interactive learning

4. **Test your solution**:
   ```bash
   python3 probabilistic_maxsat_solver.py --run-all
   ```

### 💡 Quick Tips
- Use `random.random()` for initialization
- Use `random.gauss(0, 1)` for direction
- Always move to new point (even if worse!)
- Check `INSTRUCTIONS.md` when stuck

### 🎯 Expected Performance
- Small problems: 95-100% of maximum
- Medium problems: 90-97% of maximum
- Large problems: 85-95% of maximum

---

## 🎯 What's This About?

In classical MaxSAT, you assign TRUE or FALSE to variables. But what if the world isn't so black and white? What if Hermione is **70% sure** Harry is smart, or Ron is **40% likely** to pass his exams?

That's where **Probabilistic Soft Logic** comes in! Instead of {0, 1}, we work with **[0, 1]** - continuous truth values.

## 🆚 Classical vs Probabilistic MaxSAT

### Classical MaxSAT
```
Variables: {0, 1}
Example: harryIsSmart = TRUE or FALSE
Goal: Find binary assignment maximizing satisfied clause weights
```

### Probabilistic MaxSAT (This Lab!)
```
Variables: [0, 1]
Example: harryIsSmart = 0.7 (70% true)
Goal: Find probabilistic assignment maximizing satisfied clause weights
```

## 🎲 The Hit-and-Run Algorithm

Think of it as a drunk person wandering in a box:
1. 🎯 Start at a random point in the [0,1]ⁿ hypercube
2. 🎲 Pick a random direction
3. 📏 Walk along that direction (staying in the box)
4. 🔄 Repeat, always looking for better solutions!

### Why "Hit-and-Run"?
- **Hit**: You randomly pick a direction
- **Run**: You move along that direction to explore new solutions

It's simple, elegant, and surprisingly effective!

## 📚 How Clauses Work in Probabilistic Logic

### Łukasiewicz Logic (Default)
For a clause like `{A, B, C}`:
- Satisfaction degree = min(1, truthValue(A) + truthValue(B) + truthValue(C))
- A clause is "more satisfied" when the sum of truth values is higher

### Example
```
Clause: {harryIsSmart, hermioneIsSmart, ronIsSmart} [100]

Assignment 1: [0.5, 0.5, 0.5] → satisfaction = min(1, 1.5) = 1.0 → weight = 100
Assignment 2: [0.3, 0.3, 0.3] → satisfaction = min(1, 0.9) = 0.9 → weight = 90
Assignment 3: [1.0, 0.0, 0.0] → satisfaction = min(1, 1.0) = 1.0 → weight = 100
```

For negated atoms (`-A`), we use: truthValue(-A) = 1 - truthValue(A)

## 🎯 Your Mission

Complete the `hit_and_run()` function in `probabilistic_maxsat_solver.py`:
1. Implement the Hit-and-Run algorithm
2. Find good probabilistic assignments for the given problems
3. See how your solution compares to the reference!

### 🏆 Evaluation

Your score = (Achieved Weight / Total Possible Weight) × 100%

Unlike classical MaxSAT where total weight is the sum of all clauses, in probabilistic MaxSAT, some clauses may only be partially satisfied!

## 📂 What's Provided

```
ProbabilisticMaxSAT/
├── README.md                           # This file!
├── probabilistic_maxsat_solver.py      # YOUR CODE GOES HERE
├── util.py                             # Helper classes and functions
├── visualizer.py                       # Visualize your solutions (optional)
├── problems/                           # Test problems
│   ├── hermione.txt                    # Simple Harry Potter example
│   ├── simple_*.txt                    # Small problems to debug
│   └── s2v*.txt                        # Larger benchmarks
├── reference_results.txt               # Our solution's results
└── results/                            # Your results will be saved here
```

## 🚀 Getting Started

### 1. Understand the Hermione Example
```python
# Run the example solver
python probabilistic_maxsat_solver.py
```

This will run the baseline random search on the Hermione problem.

### 2. Implement Hit-and-Run
Open `probabilistic_maxsat_solver.py` and complete the `hit_and_run()` function.

### 3. Test Your Solution
```python
# Test on all problems
python probabilistic_maxsat_solver.py --run-all
```

### 4. Visualize (Optional but Cool!)
```python
# For 2D/3D problems, visualize the search trajectory
python visualizer.py problems/hermione.txt results/hermione.res
```

## 💡 Implementation Tips

### Basic Hit-and-Run Structure
```python
def hit_and_run(problem, iterations=1000):
    # 1. Initialize with random values in [0,1]
    current = {var: random.random() for var in problem.predicates()}
    current_weight = problem.evaluate(current)
    
    for _ in range(iterations):
        # 2. Pick a random direction
        direction = random_direction()
        
        # 3. Find valid range along this direction
        t_min, t_max = compute_bounds(current, direction)
        
        # 4. Sample new point along direction
        t = random.uniform(t_min, t_max)
        candidate = move_along_direction(current, direction, t)
        
        # 5. Evaluate and maybe accept
        candidate_weight = problem.evaluate(candidate)
        if candidate_weight > current_weight:
            current = candidate
            current_weight = candidate_weight
    
    return current
```

### Key Challenges
1. **Stay in the box**: Make sure all variables remain in [0, 1]
2. **Efficient evaluation**: Cache when possible
3. **Exploration vs Exploitation**: Maybe accept worse solutions sometimes?
4. **Convergence**: Track your best solution over time

## 🎓 Learning Resources

- [Probabilistic Soft Logic Slides](https://suchanek.name/work/teaching/topics/probabilistic-soft-logic/index.html#slide-1753562882680)
- Łukasiewicz Logic: Infinite-valued logic for fuzzy reasoning
- Hit-and-Run sampling: A Markov Chain Monte Carlo (MCMC) method

## 📊 Reference Results

Our Hit-and-Run implementation achieves:
- Small problems (10 vars): ~95-98% of maximum possible
- Medium problems (20 vars): ~90-95% of maximum possible  
- Large problems (50+ vars): ~85-90% of maximum possible

Can you do better? 🏆

## 🤔 Going Further

Once you've implemented basic Hit-and-Run, try:
1. **Adaptive step size**: Adjust exploration based on progress
2. **Simulated annealing**: Accept bad moves early, get greedy later
3. **Multiple restarts**: Run from different starting points
4. **Smart initialization**: Start near promising regions
5. **Gradient hints**: Use clause weights to guide search

## 🎉 Have Fun!

This lab is **not graded** - it's about exploring probabilistic reasoning and having fun with fuzzy logic! Experiment, visualize, and see how different strategies perform.

Questions? Ideas? Found a bug? Let us know!

---
*Created with ❤️ for CSC_5AI01_TP - Logics and Symbolic AI*

