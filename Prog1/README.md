# CS 441 Programming Assignment #1

This programming assignment entails an implementation of best-first search and A* search to hanlde the 8-puzzle problem.

## Features
- Tests each of the 5 given initial states to make sure they can reach the goal state.
- Uses best-first search to get a path from each initial state to the goal state.
- Uses A* search to get a path from each initial state to the goal state.
- Each algorithm uses 3 heuristics, which use the number of misplaced tiles, the Manhattan disntances, and Euclidean distances.
- Prints findings.

## How to run
- To run the python script, assure you have both Puzzle.py and PuzzleState.py in your current directory.
- Simply run python Puzzle.py or python3 Puzzle.py depending on your version.
- This should show how each initial state is solveable, as well as the results for each algorithm and heursitic.