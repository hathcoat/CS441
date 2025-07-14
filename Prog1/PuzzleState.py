# Cody Hathcoat         July 9th, 2025          CS 441
class PuzzleState:
    def __init__(self, board, parent=None, g=0, h=0):
        self.board = list(board)  # A list of 9 elements
        self.parent = parent # For path reconstruction
        self.h = h  # Heuristic value for priority
        self.g = g # Cost so far
        self.f = g + h # Cost so far plus heuristic
    def __eq__(self, other):
        return self.board == other.board # If same boards, puzzles equal

    # Allows PuzzleState to be used in sets/dicts
    def __hash__(self):
        return hash(tuple(self.board))