import random


class Solver:
    def __init__(self):
        self.size = 3
        self.goalState = [[0,1,2], [3,4,5], [6,7,8]]



    # random numbers 1-8
    def generateRandomStartState(self):
        startState = [[0,1,2], [3,4,5], [6,7,8]]
        random.shuffle(startState)

    #goal state get
    def generateSolvableStartState(self):
        pass

    def isSolvable(self, state):
        pass


    def solve(self, startState, goalState, heuristic):
        pass


