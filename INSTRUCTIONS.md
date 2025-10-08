# 📋 Probabilistic MaxSAT - Lab Instructions

**CSC_5AI01_TP - Logics and Symbolic AI**

---

## 🎯 Objective

In this lab, you will implement the **Hit-and-Run** algorithm to solve Probabilistic MaxSAT problems. This is a practical exploration of **probabilistic soft logic** and **fuzzy reasoning**.

### What You'll Learn

- How probabilistic logic differs from classical binary logic
- The Hit-and-Run algorithm for continuous optimization
- Łukasiewicz logic and fuzzy satisfaction
- Balancing exploration and exploitation in search algorithms

---

## 📖 Background

### Classical vs Probabilistic MaxSAT

**Classical MaxSAT:**
- Variables: `{0, 1}` (Boolean)
- Goal: Find binary assignment maximizing satisfied clause weights
- Example: `harryIsSmart = TRUE` or `FALSE`

**Probabilistic MaxSAT:**
- Variables: `[0, 1]` (Continuous)
- Goal: Find probabilistic assignment maximizing weighted satisfaction
- Example: `harryIsSmart = 0.7` (70% confident Harry is smart)

### Why is this interesting?

In probabilistic logic, you can:
1. **Express uncertainty**: "I'm 80% sure it's raining"
2. **Partially satisfy clauses**: A clause can be 60% satisfied
3. **Resolve conflicts**: Instead of choosing A or ¬A, you can use A = 0.5

### Łukasiewicz Logic

We use **Łukasiewicz t-conorm** for disjunction (OR):

```
A ∨ B ∨ C = min(1, truthValue(A) + truthValue(B) + truthValue(C))
```

For negation:
```
¬A = 1 - truthValue(A)
```

**Example:**

Clause: `{A, B, C}` with weight 10

- If `A=0.4, B=0.3, C=0.2`:
  - Satisfaction degree = min(1, 0.4+0.3+0.2) = min(1, 0.9) = 0.9
  - Weighted satisfaction = 0.9 × 10 = 9.0

- If `A=0.5, B=0.5, C=0.5`:
  - Satisfaction degree = min(1, 0.5+0.5+0.5) = min(1, 1.5) = 1.0
  - Weighted satisfaction = 1.0 × 10 = 10.0

- If `A=1.0, B=0.0, C=0.0`:
  - Satisfaction degree = min(1, 1.0+0.0+0.0) = min(1, 1.0) = 1.0
  - Weighted satisfaction = 1.0 × 10 = 10.0

---

## 🎲 The Hit-and-Run Algorithm

### Intuition

Imagine you're in a dark room (the [0,1]ⁿ hypercube) looking for treasure (the optimal solution). Hit-and-Run works like this:

1. 🎯 Start at a random location
2. 🎲 Pick a random direction
3. 🚶 Walk in that direction (staying in the room)
4. 🔄 Repeat from your new position

By tracking the best position you've seen, you gradually find better solutions!

### Algorithm Details

```python
def hit_and_run(problem, iterations):
    # 1. Initialize at random point
    current = {var: random() for var in variables}
    best = current
    best_score = evaluate(current)
    
    for i in range(iterations):
        # 2. Pick random direction
        direction = random_direction()
        
        # 3. Find valid range along direction
        # We need: 0 ≤ current[v] + t*direction[v] ≤ 1 for all v
        t_min, t_max = compute_valid_range(current, direction)
        
        # 4. Sample uniformly along line
        t = uniform(t_min, t_max)
        new = current + t * direction
        
        # 5. Move to new point
        current = new
        
        # 6. Update best if better
        if evaluate(new) > best_score:
            best = new
            best_score = evaluate(new)
    
    return best
```

### Key Implementation Challenges

#### 1. Computing Valid Range

For each variable `v`, we need:
```
0 ≤ current[v] + t*direction[v] ≤ 1
```

This gives us two inequalities:
```
t ≥ -current[v] / direction[v]    (lower bound from 0)
t ≤ (1-current[v]) / direction[v]  (upper bound from 1)
```

**Watch out for:**
- Division by zero (when `direction[v] ≈ 0`)
- Sign of `direction[v]` (flips inequality)

#### 2. Random Direction

Several options:
- **Uniform on sphere**: Sample from N(0,1) and normalize
- **Coordinate-wise**: Pick one variable, set others to 0
- **Adaptive**: Weight towards promising directions

#### 3. Acceptance Strategy

Options:
- **Always move** (pure Hit-and-Run): Explore uniformly
- **Hill climbing**: Only accept improvements
- **Simulated annealing**: Accept worse moves with decreasing probability
- **Hybrid**: Combine strategies

---

## 🚀 Getting Started

### 1. Explore the Examples

```bash
# Run on Hermione example
python probabilistic_maxsat_solver.py

# Visualize a 2D problem
python visualizer.py problems/simple_2vars.txt

# See Hit-and-Run in action
python visualizer.py problems/simple_2vars.txt --animate
```

### 2. Understand the Code Structure

**Files you'll modify:**
- `probabilistic_maxsat_solver.py` - Implement `hit_and_run()` function

**Files you'll use (don't modify):**
- `util.py` - Problem, Clause, Atom classes
- `visualizer.py` - Visualization tools
- `problems/` - Test problems
- `reference_results.txt` - Target scores

### 3. Test Your Implementation

```bash
# Test on all problems
python probabilistic_maxsat_solver.py --run-all

# Compare with baseline
python probabilistic_maxsat_solver.py --compare
```

### 4. Understand the Hermione Problem

Let's analyze `problems/hermione.txt`:

```
likesHermioneRon => -likesHermioneHarry [100]
=> hermioneIsSmart [1]
hermioneIsSmart & harryIsSmart => likesHermioneHarry [3]
=> harryIsSmart [10]
=> likesHermioneRon [20]
```

**Converted to clauses:**
1. `{-likesHermioneRon, -likesHermioneHarry}` [100]
2. `{hermioneIsSmart}` [1]
3. `{-hermioneIsSmart, -harryIsSmart, likesHermioneHarry}` [3]
4. `{harryIsSmart}` [10]
5. `{likesHermioneRon}` [20]

**Analysis:**
- Clauses 2, 4, 5 are simple: they want their atoms to be 1.0
- Clause 1 (weight 100!) says: at least one of `likesHermioneRon` or `likesHermioneHarry` should be 0
- Clause 3 creates a trade-off

**Optimal strategy (binary logic):**
- Set `likesHermioneRon = 1` (satisfies clauses 1, 5)
- Set `likesHermioneHarry = 0` (helps clause 1)
- Set `harryIsSmart = 1` (satisfies clause 4)
- Clause 2 and 3 give small extra weight

**In probabilistic logic:**
- We can fine-tune values to squeeze out extra points!
- Maybe `likesHermioneHarry = 0.1` slightly helps clause 3

---

## 💡 Implementation Strategy

### Phase 1: Basic Hit-and-Run (Starter Code)

The starter code already implements a basic Hit-and-Run. **Read and understand it!**

Key components:
1. ✅ Random initialization
2. ✅ Random direction generation
3. ✅ Computing valid t range
4. ✅ Moving along direction
5. ✅ Tracking best solution

**Your task**: Make sure you understand how it works!

### Phase 2: Improvements (Optional but Fun!)

Try these improvements:

#### A. Smart Initialization
```python
# Instead of random, start near a good solution
def smart_init(problem):
    # Positive atoms with high weights should be ~1
    # Negative atoms with high weights should be ~0
    assignment = {}
    for var in problem.predicates():
        # Analyze which polarity appears more in high-weight clauses
        positive_weight = sum(c.weight for c in problem.clauses 
                             if any(a.predicate == var and a.is_positive() 
                                   for a in c.atoms))
        negative_weight = sum(c.weight for c in problem.clauses 
                             if any(a.predicate == var and a.is_negative() 
                                   for a in c.atoms))
        
        # Weight towards more important polarity
        if positive_weight > negative_weight:
            assignment[var] = 0.7 + random()*0.3
        elif negative_weight > positive_weight:
            assignment[var] = random()*0.3
        else:
            assignment[var] = random()
    
    return assignment
```

#### B. Simulated Annealing
```python
def hit_and_run_with_annealing(problem, iterations):
    current = random_init()
    best = current
    best_score = evaluate(current)
    
    for i in range(iterations):
        temperature = 1.0 - (i / iterations)  # Cool down over time
        
        new = hit_and_run_step(current)
        new_score = evaluate(new)
        
        # Accept if better, or with probability based on temperature
        if new_score > evaluate(current):
            current = new
        elif random() < exp((new_score - evaluate(current)) / temperature):
            current = new  # Accept worse solution (exploration)
        
        if new_score > best_score:
            best = new
            best_score = new_score
    
    return best
```

#### C. Adaptive Step Size
```python
def adaptive_hit_and_run(problem, iterations):
    # Start with large steps (exploration)
    # Decrease step size over time (exploitation)
    
    for i in range(iterations):
        progress = i / iterations
        
        # Sample t from smaller range as we progress
        t_range = (1.0 - progress) * (t_max - t_min)
        t_mid = (t_max + t_min) / 2
        t = uniform(t_mid - t_range/2, t_mid + t_range/2)
        
        # ... rest of algorithm
```

#### D. Multiple Restarts
```python
def hit_and_run_with_restarts(problem, iterations, num_restarts=5):
    best_overall = None
    best_score = float('-inf')
    
    for restart in range(num_restarts):
        solution = hit_and_run(problem, iterations // num_restarts)
        score = evaluate(solution)
        
        if score > best_score:
            best_overall = solution
            best_score = score
    
    return best_overall
```

---

## 🧪 Testing Strategy

### 1. Start Small

Test on simple problems first:
```bash
python probabilistic_maxsat_solver.py  # Hermione
python visualizer.py problems/simple_2vars.txt --animate
```

### 2. Debug with Visualization

For 2-variable problems, use the visualizer:
```bash
# Run solver
python probabilistic_maxsat_solver.py

# Visualize result
python visualizer.py problems/simple_2vars.txt results/simple_2vars.res
```

### 3. Understand Edge Cases

**Conflicting clauses** (`problems/conflicting.txt`):
```
{A} [10]
{-A} [10]
```

In binary logic: Can satisfy only one (max score = 50%)
In probabilistic logic: Set A = 0.5, both clauses get 0.5 satisfaction!

### 4. Check Progress

```bash
# See how your solution compares
python probabilistic_maxsat_solver.py --run-all

# Compare strategies
python probabilistic_maxsat_solver.py --compare
```

---

## 📊 Expected Performance

Your Hit-and-Run implementation should achieve:

| Problem Size | Expected Score | Time |
|--------------|---------------|------|
| Small (2-5 vars) | 95-100% | < 1s |
| Medium (10-20 vars) | 90-97% | 1-5s |
| Large (20+ vars) | 85-95% | 5-30s |

**Notes:**
- Scores are relative to maximum possible weight
- Randomness means results will vary between runs
- More iterations generally = better results (but slower)

---

## 🎓 Concepts to Explore

### 1. Why Does Hit-and-Run Work?

- **Uniform sampling**: Over many iterations, explores the space uniformly
- **Markov Chain**: Each step depends only on current position
- **Convergence**: Given enough time, finds optimal solution (in expectation)

### 2. Exploration vs Exploitation Trade-off

- **Exploration**: Try different regions to find good areas
- **Exploitation**: Focus on promising regions to optimize

Hit-and-Run balances these:
- Long steps → more exploration
- Short steps → more exploitation
- Random direction → avoid getting stuck

### 3. Comparison with Other Algorithms

| Algorithm | Pros | Cons |
|-----------|------|------|
| Random Search | Simple | Very slow |
| Hill Climbing | Fast locally | Gets stuck |
| Simulated Annealing | Good global search | Needs tuning |
| **Hit-and-Run** | **Simple + Effective** | **Needs many iterations** |
| Gradient Descent | Very fast | Needs gradients |

---

## 🎯 Submission (This is a non-graded lab!)

This lab is **not graded** - it's for learning! However, if you want to share your work:

1. Make sure your `hit_and_run()` function is complete
2. Run it on all problems: `python probabilistic_maxsat_solver.py --run-all`
3. Check your results in the `results/` folder
4. Compare with `reference_results.txt`

**Optional challenges:**
- Beat the reference results!
- Implement advanced strategies (annealing, restarts, etc.)
- Create your own interesting problems
- Visualize your algorithm's behavior

---

## 🤔 Discussion Questions

Think about these as you work:

1. **What makes a good starting point?** Random vs. smart initialization?

2. **How many iterations are enough?** How can you tell if you've converged?

3. **Why are some problems harder than others?** What makes a problem difficult?

4. **How does probabilistic logic help with conflicting rules?** Compare `problems/conflicting.txt` in binary vs. probabilistic logic.

5. **Could you use gradients?** The objective function is differentiable - why not use gradient ascent?

6. **What about local optima?** Does Hit-and-Run get stuck like hill climbing?

---

## 📚 Resources

### Papers & Slides
- [Probabilistic Soft Logic - Fabian Suchanek](https://suchanek.name/work/teaching/topics/probabilistic-soft-logic/index.html#slide-1753562882680)
- [Hit-and-Run Sampling - Smith (1984)](https://www.jstor.org/stable/3689711)
- [Łukasiewicz Logic - Stanford Encyclopedia](https://plato.stanford.edu/entries/logic-manyvalued/)

### Python Tips
```python
# Generate random direction
import random
direction = {var: random.gauss(0, 1) for var in variables}

# Normalize direction
import math
length = math.sqrt(sum(d*d for d in direction.values()))
direction = {var: d/length for var, d in direction.items()}

# Clamp values to [0,1]
value = max(0.0, min(1.0, value))
```

---

## ❓ FAQ

**Q: My solver is too slow!**
- Reduce iterations for testing
- Profile your code to find bottlenecks
- Cache evaluations if you check the same solution multiple times

**Q: I keep getting invalid solutions (values outside [0,1])!**
- Check your t_min/t_max computation
- Make sure to handle division by zero
- Use clamping as a safety net: `max(0.0, min(1.0, value))`

**Q: My scores are much worse than the reference!**
- Make sure you're finding the maximum (not minimum)
- Try more iterations
- Check that you're keeping the best solution found
- Debug on simple problems first

**Q: Can I use external libraries?**
- For core implementation: Only standard library (random, math)
- For experimentation: Sure! Try numpy, scipy, etc.

**Q: The conflicting problem gives 53% score - is this right?**
- Yes! With `{A}[10]` and `{-A}[10]`, best is A=0.5, giving 0.5×10 + 0.5×10 = 10 out of 20 total = 50%. Plus the B clauses help a bit.

**Q: How is this different from fuzzy logic?**
- Very similar! Łukasiewicz logic is a type of fuzzy logic
- We use continuous truth values [0,1]
- We use fuzzy operators (Łukasiewicz t-conorm for OR)

---

## 🎉 Have Fun!

Remember, this is about learning and exploring! Don't stress about perfect scores - focus on understanding:
- How probabilistic logic works
- How Hit-and-Run explores the space
- The trade-offs in algorithm design

Questions? Ideas? Found something cool? Share with the class!

---

*Lab created with ❤️ for CSC_5AI01_TP - Logics and Symbolic AI*
*Based on research in Probabilistic Soft Logic and Fuzzy Reasoning*

**Acknowledgments:**
- Prof. Fabian Suchanek for the course and Hit-and-Run suggestion
- Original MaxSAT lab creators
- The students - have fun exploring!

