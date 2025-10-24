import random
from heuristics import Heuristics

class Solver:
    def __init__(self):
        self.size = 3
        self.goalState = ((0,1,2), (3,4,5), (6,7,8))

        self.heuristic = Heuristics(self.goalState)


    def generateRandomSolvableBoard(self):
        flattenedBoard = list(range(self.size * self.size))

        while True:
            random.shuffle(flattenedBoard)

            state = []

            for i in range(0,self.size * self.size, self.size):
                state.append(flattenedBoard[i : i + self.size])

            if self.isSolvable(state):
                return tuple(tuple(row) for row in state)


    def neighbors(self):
        pass

    def isSolvable(self, state):
        inversionCounter = 0
        flattenedState = []

        for row in state:
            for tile in row:
                flattenedState.append(tile)

        for i in range(len(flattenedState)):
            for j in range(i+1,len(flattenedState)):
                tileI =flattenedState[i]
                tileJ = flattenedState[j]
                if tileI != 0 and tileJ != 0 and tileI > tileJ:
                    inversionCounter += 1

        return inversionCounter % 2 == 0


    def calculateCosts(self):
        pass

    def runBenchmark(self):
        pass

    def solve(self, startState, goalState, heuristic):
        pass


if __name__ == "__main__":

    solver = Solver()

    print("isSolvable Test")

    solvable_state = [
        [7, 2, 4],
        [5, 0, 6],
        [8, 3, 1]
    ]
    unsolvable_state = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0]
    ]
    print(f"solvable state is solvable: {solver.isSolvable(solvable_state)}")
    print(f"unsolvable state is solvable: {solver.isSolvable(unsolvable_state)}")
    print()

    print("generateRandomSolvableBoard Test")

    for i in range(3):
        print(f"Generated board {i + 1}")
        board = solver.generateRandomSolvableBoard()

        isSolvable = solver.isSolvable(board)
        print(board)
        print(f"board is solvable: {isSolvable}\n")

        if not isSolvable:
            print("TEST FAILED: Generated board is not solvable")
