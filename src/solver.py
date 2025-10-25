import heapq
import random
import time
import statistics
from datetime import datetime
from heuristics import Heuristics

# helper to flatten 2D board to 1D
def flatten(state):
    """
    Flatten a 2D board (tuple of tuples) into a 1D list

    Parameters
            state: tuple[tuple[int]]
                current board configuration

    Returns: List of ints representing the flattened state
    """
    return [tile for row in state for tile in row]

class Solver:
    """
    A* 8-Puzzle Solver

    Uses A* search with either Manhattan or Hamming distance as heuristic
    goal is to find an optimal solution
    """

    def __init__(self):
        """
        Constructor

        Initialize solver with a 3x3 goal state and heuristic object
        """
        self.size = 3
        self.goalState = ((0,1,2), (3,4,5), (6,7,8))
        self.heuristic = Heuristics(self.goalState)

    def generateRandomSolvableBoard(self):
        """
        Generate random solvable board as a tuple of tuples

        Returns: tuple[tuple[int]]
            random solvable board configuration
        """
        # range generates list from 0-8
        flattenedBoard = list(range(self.size * self.size))

        # as long till it returns something
        while True:
            # shuffles list
            random.shuffle(flattenedBoard)

            # If solvable convert each row to a tuple and return
            if self.isSolvable(flattenedBoard):
                state = []

                # converting 1D board into 2D board
                for i in range(0,self.size * self.size, self.size):
                    state.append(flattenedBoard[i : i + self.size])

                return tuple(tuple(row) for row in state)

    def isSolvable(self, state):
        """
        Check solvability by counting inversions

        Parameters
        state : list[int]
            flattened 3x3 board (length 9)

        Returns: bool (True if solvable, else False)
        """
        inversionCounter = 0

        # iterating through the list
        for i in range(len(state)):
            # iterating through the list what follows after the i in this list
            for j in range(i+1,len(state)):
                # number we are comparing to the rest that follows after
                tileI = state[i]
                tileJ = state[j]
                if tileI != 0 and tileJ != 0 and tileI > tileJ:
                    inversionCounter += 1

        return inversionCounter % 2 == 0

    # generate all possible moves (up, down, left, right) from current state
    def neighbors(self, state):
        """
        Generate all valid neighbor states by sliding the blank (0) up/down/left/right.

        Parameters
            state: tuple[tuple[int]]
                current board configuration

        Returns: list[tuple[tuple[int]]]
            all reachable states
        """

        neighbors = []
        blankState = None

        # find blank position
        for row in range(self.size):
            for col in range(self.size):
                if state[row][col] == 0:
                    blankState = (row, col)
                    break
            if blankState is not None:
                break

        blank_row, blank_col = blankState

        # possible moves: (row change, col change)
        moves = {
            'U': (-1, 0),   # up
            'D': (1, 0),    # down
            'L': (0, -1),   # left
            'R': (0, 1)     # right
        }

        for move, (mr, mc) in moves.items():
            new_row = blank_row + mr
            new_col = blank_col + mc

            # check if move is inside board
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                # create new board as list and converts tuples to lists
                new_board = [list(row) for row in state]
                # swap blank with target tile (a, b = b, a)
                new_board[blank_row][blank_col], new_board[new_row][new_col] = new_board[new_row][new_col], \
                new_board[blank_row][blank_col]
                # convert back to tuple of tuples
                neighbors.append(tuple(tuple(row) for row in new_board))

        return neighbors

    def calculateCosts(self, state, g, heuristic):
        """
        Calculate total cost f = g + h for a given state
        g(n): number of moves from the start state
        h(n): heuristic estimate from state to goal
        f(n): total estimated cost of path through n

        Parameters
        state: tuple[tuple[int]]
            current puzzle configuration
        g: int
            cost of moves so far
        heuristic: string
            which heuristic to use: "manhattan" or "hamming"

        Returns: f, g, h - tuple[int, int, int]
            f = total estimated cost
            g = path cost so far
            h = heuristic estimate
        """

        if heuristic == "manhattan":
            h = self.heuristic.manhattan(state)
        elif heuristic == "hamming":
            h = self.heuristic.hamming(state)
        else:
            raise ValueError(f"Unknown heuristic: {heuristic}")

        return g + h, g, h

    def solve(self, startState, goalState, heuristic):
        """
        Solve the 8-puzzle using A* search.

        Parameters
        startState: tuple[tuple[int]]
            starting board configuration
        goalState: tuple[tuple[int]]
            target board configuration
        heuristic: string
            which heuristic to use: "manhattan" or "hamming"

        Returns: tuple[list[tuple[tuple[int]]], int]
            path: list[tuple[tuple[int]]]
                sequence of states from start to goal
            nodesExpanded: int
                number of nodes expanded during search
        """

        # priority queue: stores (f, g, state, path)
        openList = []
        # all states we've already visited, without duplicates
        closedSet = set()

        # initial costs
        f, g, h = self.calculateCosts(startState, g=0, heuristic=heuristic)
        # push starting node into the openList
        heapq.heappush(openList, (f, g, startState, [startState]))

        nodesExpanded = 0

        # as long as there are nodes to explore
        while openList:
            # get state info with smallest f
            f, g, currentState, path = heapq.heappop(openList)

            # if goal reached = done
            if currentState == goalState:
                return path, nodesExpanded

            # avoid re-expanding
            if currentState in closedSet:
                continue
            closedSet.add(currentState)

            nodesExpanded += 1

            # generate neighbors
            for neighbor in self.neighbors(currentState):
                if neighbor not in closedSet:
                    new_g = g + 1
                    # we just need f so we don't care about g and h
                    f, _, _ = self.calculateCosts(neighbor, new_g, heuristic)
                    heapq.heappush(openList, (f, new_g, neighbor, path + [neighbor]))

        return None, nodesExpanded


    # run 100 random solvable states per heuristic, measure time & nodes, compute statistics
    def runBenchmark(self):
        """
        Run A* search on 100 random solvable boards for both heuristics
        and measure performance (runtime + memory effort)

        Returns: dict
            statistics for each heuristic (runtime and nodes expanded)
        """

        numTests = 100
        heuristics = ["manhattan", "hamming"]
        results = {}

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("../results/memory_usage", "a") as mem_file, open("../results/run_times", "a") as run_file:
            for heuristic in heuristics:

                runtimes = []
                nodesExpandedList = []

                for i in range(numTests):
                    startState = self.generateRandomSolvableBoard()

                    # get current time
                    start_time = time.time()

                    path, nodesExpanded = self.solve(startState, self.goalState, heuristic)
                    end_time = time.time()

                    # calculate time needed
                    runtime = end_time - start_time

                    # add the outcome
                    runtimes.append(runtime)
                    nodesExpandedList.append(nodesExpanded)

                # calculate statistics after 100 runs are finished
                results[heuristic] = {
                    # average runtime
                    "mean_runtime": statistics.mean(runtimes),
                    # standard deviation of runtime
                    "standard_runtime": statistics.stdev(runtimes),
                    # average number of nodes expanded (memory effort)
                    "mean_nodes": statistics.mean(nodesExpandedList),
                    # standard deviation of nodes expanded
                    "standard_nodes": statistics.stdev(nodesExpandedList)
                }

                # write results to files
                mem_file.write(
                    f"{timestamp} - Heuristic: {heuristic}, Mean nodes: {results[heuristic]['mean_nodes']:.2f}, Standard nodes: {results[heuristic]['standard_nodes']:.2f}\n")
                run_file.write(
                    f"{timestamp} - Heuristic: {heuristic}, Mean runtime: {results[heuristic]['mean_runtime']:.4f} s, Standard runtime: {results[heuristic]['standard_runtime']:.4f} s\n")

        return results

# TESTING
if __name__ == "__main__":

    solver = Solver()

    print("isSolvable Class Test")

    solvable_state = [7, 2, 4, 5, 0, 6, 8, 3, 1]
    unsolvable_state = [1, 2, 3, 4, 5, 6, 8, 7, 0]

    print("solvable state is solvable:", solver.isSolvable(solvable_state))
    print("unsolvable state is solvable:", solver.isSolvable(unsolvable_state), "\n")

    print("generateRandomSolvableBoard Test")

    for i in range(3):
        board = solver.generateRandomSolvableBoard()
        isSolvable = solver.isSolvable(flatten(board))

        print(f"Board {i + 1}:", board)
        print("Solvable:", isSolvable)
        print("Neighbors:", len(solver.neighbors(board)), "\n")

        if not isSolvable:
            print("TEST FAILED: Generated board is not solvable")
    print()

    print("A* Solver Test")
    start = ((1, 2, 3),
             (4, 0, 6),
             (7, 5, 8))
    goal = solver.goalState

    path, expanded = solver.solve(start, goal, "manhattan")
    print(f"Manhattan solved it in {len(path) - 1} moves (expanded {expanded} nodes)")

    path, expanded = solver.solve(start, goal, "hamming")
    print(f"Hamming solved it in {len(path) - 1} moves (expanded {expanded} nodes)")

    solver.runBenchmark()