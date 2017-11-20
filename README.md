# Vehicle Routing Problem with Time Window Solver with GA

Language : Python3

## Assumption

- One single depot
- All vehicles have the same capacity

## Dataset

http://w.cba.neu.edu/~msolomon/problems.htm

## Python Libraries

### Output Data

- matplotlib.pyplot
- networkx

### Others

- time
- numpy
- random
- copy
- math

## Technique

### Selection
- Weight Sum method
- Rank Sum method
- Pareto Ranking Selection

### Crossover

- Uniform Order Crossover (UOX)
- Route Crossover (RC)
- Best Cost Route Crossover (BCRC)

### Mutation

- Inversion Mutation

## Execution

Default
```
python3 main.py
```
Use dataset/R1/R101.txt

Give Dataset  
ex)
```
python3 main.py dataset/C2/C203.txt
```
