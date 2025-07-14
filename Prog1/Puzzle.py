# Cody Hathcoat         July 9th, 2025          CS 441
import itertools
import math
from PuzzleState import PuzzleState
from heapq import heappush, heappop

counter = itertools.count() #Hanldes tibreaker so heapq works if = h(n)
max_steps = 1000000

# Generate puzzle states that can exist from moving block
def get_successors(state):
    index = state.board.index('b') # Find blank spot
    moves = [] # successor states
    row, col = divmod(index, 3) #consider list as 3x3

    #How the index changes if you move 'b' (Up/down a row is +- 3, Left/Right a col is +- 1)
    directions = {
        'up': -3, 'down': 3, 'left': -1, 'right': 1
    }

    #Try each of the 4 directions
    for move, delta in directions.items():
        new_index = index + delta

        #Hanlde edge conditions
        if move == 'left' and col == 0:
            continue
        if move == 'right' and col == 2:
            continue
        if move == 'up' and row == 0:
            continue
        if move == 'down' and row == 2:
            continue

        # new_board = list(state.board)
        # new_board[index], new_board[new_index] = new_board[new_index], new_board[index]
        # new_board = tuple(new_board)
        new_board = state.board[:] # Copy board list
        #Swap blank with target (Simulate a move)
        new_board[index], new_board[new_index] = new_board[new_index], new_board[index]
        # Create new state with parent as current state
        moves.append(PuzzleState(new_board, parent=state))

    return moves

# Heuristic 1: Number of misplaced
def h_misplaced(state):
    goal = ['1', '2', '3', '4', '5', '6', '7', '8', 'b']
    count = 0
    i = 0
    while i < len(goal):
        if state.board[i] != goal[i]:
            count += 1
        i += 1
    return count

#Heuristic 2: Manhattan
def h_manhattan(state):
    goal_positions = {
        '1': (0, 0), '2': (0, 1), '3': (0, 2), 
        '4': (1, 0), '5': (1, 1), '6': (1, 2),
        '7': (2, 0), '8': (2, 1), 'b': (2, 2)
    }
    distance = 0

    for idx, tile in enumerate(state.board):
        if tile == 'b':
            continue
        curr_row, curr_col = divmod(idx, 3)
        goal_row, goal_col = goal_positions[tile]
        #Increase the manhattan distance for that tile
        distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance

#Heuristic 3: Euclidean
def h_euclidean(state):
    goal_positions = {
        '1': (0, 0), '2': (0, 1), '3': (0, 2), 
        '4': (1, 0), '5': (1, 1), '6': (1, 2),
        '7': (2, 0), '8': (2, 1), 'b': (2, 2)
    }
    distance = 0.0

    for idx, tile in enumerate(state.board):
        if tile == 'b':
            continue # Skip the blank spot
        curr_row, curr_col = divmod(idx, 3)
        goal_row, goal_col = goal_positions[tile]

        dx = curr_row - goal_row
        dy = curr_col - goal_col
        distance += math.sqrt(dx*dx + dy*dy)
    return distance

def best_first_search(start_board, heuristic_fn):
    start = PuzzleState(start_board)
    start.h = heuristic_fn(start)
    
    frontier = [start] # Serve as priority queue
    explored = [] #List of seen boards
    steps = 0

    # Loop while there's nodes to explore
    while frontier:
        #Limit the number of steps
        if steps >= max_steps:
            print(f"Stopped after {max_steps} nodes - no solution found.")
            return None

        #Sort frontier by heuristic val (like priority queue)
        frontier.sort(key=lambda state: state.h)
        current = frontier.pop(0) #Pop state with lowest h(n)
        steps += 1

        #If goal found
        if current.board == ['1', '2', '3', '4', '5', '6', '7', '8', 'b']:
            return reconstruct_path(current)
        
        explored.append(current.board) # Don't reprocess the state

        #Create a neighboor state and evaluate its heuristic
        for neighbor in get_successors(current):
            neighbor.h = heuristic_fn(neighbor)

            #If not explored and not in frontier, add it.
            if neighbor.board not in explored and all(neighbor.board != s.board for s in frontier):
                frontier.append(neighbor)
    return None


def a_star_search(start_board, heuristic_fn):
    #Initialies start state.
    start = PuzzleState(start_board)
    start.g = 0 #Cost from start to current node.
    start.h = heuristic_fn(start) #Heuristic cost to goal
    start.f = start.g + start.h #Total estimate cose.

    counter = itertools.count() #Unique sequence count for tie breakers
    frontier = [] #Act as priority queue of (f, count, state)
    heappush(frontier, (start.f, next(counter), start)) #Push the start node.

    explored = {} #Maps board state to lowest g value seen
    steps = 0 #Number expanded nodes

    #Keep exploring the lowest f-cost nodes.
    while frontier:
        if steps >= max_steps:
            print(f"Stopped after {max_steps} nodes - no solution found.")
            return None #Prevent infinite loops

        _, _, current = heappop(frontier) #Get lowest f-score
        steps += 1

        #Is the goal reached?
        if current.board == ['1', '2', '3', '4', '5', '6', '7', '8', 'b']:
            return reconstruct_path(current) #Must backtrack

        board_key = tuple(current.board) #Convert for dict look up

        #Skip if board is already explored with better or equal g
        if board_key in explored and explored[board_key] <= current.g:
            continue
        explored[board_key] = current.g #Update with best g

        #Generate and evaluate all valid next states
        for neighbor in get_successors(current):
            neighbor.g = current.g + 1
            neighbor.h = heuristic_fn(neighbor)
            neighbor.f = neighbor.g + neighbor.h

            board_key = tuple(neighbor.board)
            #Only add to frontier if its a better path
            if board_key not in explored or neighbor.g < explored[board_key]:
                heappush(frontier, (neighbor.f, next(counter), neighbor))

    return None

# Once goal hit, walk back through parent links.
def reconstruct_path(state):
    path = []
    while state:
        path.append(state.board)
        state = state.parent
    path.reverse()
    return path

#Return the number of  inversions
def count_inversions(board):
    tiles = [tile for tile in board if tile != 'b'] #Disregard blank spot
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions

#Determine if a given goal is reachable by a state.
def is_solvable(start, goal):
    start_inv = count_inversions(start)
    goal_inv = count_inversions(goal)
    return (start_inv % 2) == (goal_inv % 2) 

#Check if all states are solvable.
def check_states(s1, s2, s3, s4, s5, sG):
    if is_solvable(s1, sG):
        print("State 1 is solvable")
    else:
        print("State 1 is not solvable")
        return

    if is_solvable(s2, sG):
        print("State 2 is solvable")
    else:
        print("State 2 is not solvable")
        return

    if is_solvable(s3, sG):
        print("State 3 is solvable")
    else:
        print("State 3 is not solvable")
        return

    if is_solvable(s4, sG):
        print("State 4 is solvable")
    else:
        print("State 4 is not solvable")
        return

    if is_solvable(s5, sG):
        print("State 5 is solvable")
    else:
        print("State 5 is not solvable")
        return

def main():
    state1 = ['1', '2', '3', '4', '5', '6', '7', 'b', '8'] # Simple case
    state2 = ['1', '2', '3', '4', '5', '6', 'b', '7', '8']
    state3 = ['5', '4', '6', 'b', '8', '1', '7', '2', '3']
    state4 = ['6', '4', '7', '8', '5', 'b', '3', '2', '1']
    state5 = ['2', '5', '4', '3', '1', '6', 'b', '8', '7']
    goal = ['1', '2', '3', '4', '5', '6', '7', '8', 'b']

    test_states = [state1, state2, state3, state4, state5]

    check_states(state1, state2, state3, state4, state5, goal)

    heuristics = [
        ("Misplaced Tiles", h_misplaced),
        ("Manhattan Distance", h_manhattan),
        ("Euclidean Distance", h_euclidean),
    ]

    state_num = 0
    for state in test_states:
        state_num += 1
        print(f"\nState # {state_num}")

        for name, fn in heuristics:
            print(f"\n*****Heuristic: {name}*****")
            best_first_path = best_first_search(state, fn)
            a_star_solution_path = a_star_search(state, fn)

            if best_first_path:
                print(f"\nBest First Solution Path for {name} ({len(best_first_path)} steps):")
                for step in best_first_path:
                    print(step)
            else:
                print("No solution found for Best First.")

            if a_star_solution_path:
                print(f"\nA* Solution Path for {name} ({len(a_star_solution_path)} steps):")
                for step in a_star_solution_path:
                    print(step)
            else:
                print("No solution found for A*.")

if __name__ == "__main__":
    main()