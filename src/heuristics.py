class Heuristics:

    def __init__(self, goalState):
        self.size = len(goalState)

        #hashmap key: tile name (number), value: position on board
        self.goalStatePositions = {}

        for row in range(self.size):
            for col in range(self.size):
                tile = goalState[row][col]
                self.goalStatePositions[tile] = (row, col)



    def manhattanDistance(self,state):
        manhattan = 0
        for row in range(self.size):
            for col in range(self.size):
                tile = state[row][col]

                if tile != 0:  #self.goalStatePositions[0][0] to specify position regardless of number
                    positionTile = self.goalStatePositions[tile]
                    goalRow = positionTile[0]
                    goalCol = positionTile[1]
                    manhattan += abs(row - goalRow) + abs(col - goalCol)
        return manhattan

if __name__ == "__main__":
    print("manhattan Distance test")
    goalState = [[0,1,2],
                 [3,4,5],
                 [6,7,8]]
    startState1 = ((7,2,4),
                   (5,0,6),
                   (8,3,1))
    startState2 = ((5,1,8),
                   (3,0,6),
                   (2,4,7))

    heuristicsCalculator = Heuristics(goalState)
    manhattanDistance1 = heuristicsCalculator.manhattanDistance(startState1)
    manhattanDistance2 = heuristicsCalculator.manhattanDistance(startState2)

    print(manhattanDistance1)
    print(manhattanDistance2)

