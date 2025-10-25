class Heuristics:
    """
    A class for heuristic functions used in the 8-puzzle problem
    Stores goal positions of each tile and computes manhattan/hamming distance
    """

    def __init__(self, goalState):
        """
        Constructor
        builds a mapping (dictionary) of tile numbers to their positions in the goal state

        Parameters
        goalState : tuple[tuple[int]]
            goal board configuration

        Attributes
        size : int
            board dimension (e.g., 3 for 3x3 puzzle)
        goalStatePositions : dict[int, tuple[int, int]]
            maps each tile value to its goal (row, col) position
        """

        # stores goalState
        self.size = len(goalState)

        # enforce tuples
        self.goalState = tuple(tuple(row) for row in goalState)

        # empty dictionary - hashmap key: tile name (number), value: position on board
        self.goalStatePositions = {}

        for row in range(self.size):
            for col in range(self.size):
                tile = goalState[row][col]
                self.goalStatePositions[tile] = (row, col)

    def _validate_state(self, state):
        """
        helper to ensure the given state matches the expected board size
        """
        if len(state) != self.size:
            raise ValueError(f"State size {len(state)} does not match goal size {self.size}")
        for row in state:
            if len(row) != self.size:
                raise ValueError("One or more rows in the state have incorrect length.")

    def manhattan(self, state):
        """
        Computes manhattan distance heuristic
        Sum of absolute row + column differences between each tile and its goal position

        Parameters
        goal state : list[list[int]]
        state: tuple[tuple[int]]
            Current puzzle configuration

        Returns: int (total manhattan distance)

        Complexity
        Time: O(n^2)
        """
        self._validate_state(state)

        # Initialization
        manhattan = 0

        for row in range(self.size):
            for col in range(self.size):
                # getting state number on a position
                tile = state[row][col]

                if tile != 0:  #self.goalStatePositions[0][0] to specify position regardless of number
                    # looks up goal coordinates of the tile and afterward separates into Row and Col
                    goalPosition = self.goalStatePositions[tile]
                    goalRow = goalPosition[0]
                    goalCol = goalPosition[1]
                    manhattan += abs(row - goalRow) + abs(col - goalCol)
        return manhattan

    def hamming(self, state):
        """
        Computes hamming distance heuristic
        Counts how many tiles are not in their goal position

        Parameters
        state : list[list[int]] or tuple[tuple[int]]
            Current puzzle configuration

        Returns: int (number of misplaced tiles)

        Complexity
        Time: O(n^2)
        """
        self._validate_state(state)

        # Initialization
        hamming = 0

        for row in range(self.size):
            for col in range(self.size):
                # getting IS-number of current row/col
                tile = state[row][col]

                if tile != 0:
                    # looking if SHOULD-Position of current tile is current row/col
                    if self.goalStatePositions[tile] != (row, col):
                        hamming += 1
        return hamming

# TESTING
if __name__ == "__main__":
    print("heuristics Class Test")
    goalState = ((0,1,2),
                 (3,4,5),
                 (6,7,8))
    startState1 = ((7,2,4),
                   (5,0,6),
                   (8,3,1))
    startState2 = ((5,1,8),
                   (3,0,6),
                   (2,4,7))

    heuristicsCalculator = Heuristics(goalState)

    manhattanDistance1 = heuristicsCalculator.manhattan(startState1)
    manhattanDistance2 = heuristicsCalculator.manhattan(startState2)
    manhattanDistance3 = heuristicsCalculator.manhattan(goalState)
    hammingDistance1 = heuristicsCalculator.hamming(startState1)
    hammingDistance2 = heuristicsCalculator.hamming(startState2)
    hammingDistance3 = heuristicsCalculator.hamming(goalState)

    print("Manhattan Test")
    print(manhattanDistance1)
    print(manhattanDistance2)
    print("Should be zero (goalState):", manhattanDistance3)

    print("Hamming Test")
    print(hammingDistance1)
    print(hammingDistance2)
    print("Should be zero (goalState):", hammingDistance3)

