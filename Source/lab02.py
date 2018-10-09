# for arguments
import sys

import math


# Point object to show where in the map
class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def EuclideanDistance(self, point):
        return math.sqrt((point.row - self.row) * (point.row - self.row) +
                         (point.col - self.col) * (point.col - self.col))

    def isSame(self, point):
        return self.row == point.row and self.col == point.col


# PointMore object not only show where in the mao
# but also show its parent, its cost
class PointMore:
    def __init__(self, point):
        self.point = point
        self.parent = None
        self.cost = 0

    def setParent(self, parent):
        self.parent = parent

    def setCost(self, cost):
        self.cost = cost

    def addCost(self, moreCost):
        self.cost += moreCost

    def print(self):
        print(self.point.row, self.point.col, self.cost)


# PriorityQueue object for store PointMore
# lower cost mean higher priority to be pulled out
class PriorityQueue:
    def __init__(self):
        self.data = []

    def print(self):
        for i in self.data:
            i.print()

    def isEmpty(self):
        # empty sequences are false
        return not self.data

    def add(self, newPointMore):
        # only add new PointMore if not exist in data
        # if exist, only replace of new PointMore has lower cost
        exist = False
        for pointMore in self.data:
            if pointMore.point.isSame(newPointMore.point):
                exist = True
                if pointMore.cost > newPointMore.cost:
                    pointMore.setCost(newPointMore.cost)
                break
        if not exist:
            self.data.append(newPointMore)

    def pullLowest(self):
        if self.isEmpty():
            return
        # find PointMore which has lowest cost to be pulled
        lowestCostIndex = 0
        for i in range(1, len(self.data)):
            if self.data[i].cost < self.data[lowestCostIndex].cost:
                lowestCostIndex = i
        return self.data.pop(lowestCostIndex)


class PathMap:
    # Example
    # 1 0 0
    # 0 1 0
    # 0 1 0
    # 1 is obstacle, 0 is not
    def __init__(self, f, size):
        self.size = size
        self.data = []
        for line in f:
            row = []
            for word in line.split():
                row.append(int(word))
            self.data.append(row)

    def printSize(self):
        print(self.size)

    def printMap(self):
        for row in self.data:
            for num in row:
                print(num, end=' ')
            # print() itself will print new line
            print()

    # check if size and data read from file is equal
    def isValid(self):
        if len(self.data) != self.size:
            return False
        for row in self.data:
            if len(row) != self.size:
                return False
        return True

    # return true if point in map and not obstacle
    # otherwise return false
    def isMovablePoint(self, point):
        # check if point in map
        if point.row < 0 or point.row >= self.size or point.col < 0 or point.col >= self.size:
            return False
        # check if point is obstacle
        if self.data[point.row][point.col] == 1:
            return False
        return True

    # next move of p is point 1 -> 8
    # valid move if next point is in map and not obstacle
    # return list of valid next move
    # 1 2 3
    # 8 p 4
    # 7 6 5
    def nextMove(self, point):
        listNextMove = []
        # 1 2 3
        if self.isMovablePoint(Point(point.row - 1, point.col - 1)):
            listNextMove.append(Point(point.row - 1, point.col - 1))
        if self.isMovablePoint(Point(point.row - 1, point.col)):
            listNextMove.append(Point(point.row - 1, point.col))
        if self.isMovablePoint(Point(point.row - 1, point.col + 1)):
            listNextMove.append(Point(point.row - 1, point.col + 1))
        # 4
        if self.isMovablePoint(Point(point.row, point.col + 1)):
            listNextMove.append(Point(point.row, point.col + 1))
        # 5 6 7
        if self.isMovablePoint(Point(point.row + 1, point.col + 1)):
            listNextMove.append(Point(point.row + 1, point.col + 1))
        if self.isMovablePoint(Point(point.row + 1, point.col)):
            listNextMove.append(Point(point.row + 1, point.col))
        if self.isMovablePoint(Point(point.row + 1, point.col - 1)):
            listNextMove.append(Point(point.row + 1, point.col - 1))
        # 8
        if self.isMovablePoint(Point(point.row, point.col - 1)):
            listNextMove.append(Point(point.row, point.col - 1))
        return listNextMove

    def printNextMove(self, point):
        for move in self.nextMove(point):
            print(move.row, move.col)


class PathProblem:
    # get value from file
    # size
    # start_row,start_col
    # goal_row,goal_col
    # ...
    def __init__(self, f):
        # split for line to split to word
        size = int(f.readline())

        startPointData = f.readline().split(',')
        x = int(startPointData[0])
        y = int(startPointData[1])
        self.startPoint = Point(x, y)

        goalPointData = f.readline().split(',')
        x = int(goalPointData[0])
        y = int(goalPointData[1])
        self.goalPoint = Point(x, y)

        self.pathMap = PathMap(f, size)

    def print(self):
        self.pathMap.printSize()
        print(self.startPoint.row, self.startPoint.col)
        print(self.goalPoint.row, self.goalPoint.col)
        self.pathMap.printMap()


# return file if open success
# if fail, return None
def openWithError(filename, mode):
    try:
        f = open(filename, mode)
        return f
    except Exception as e:
        print(e)


def main():
    # 3 arguments
    if len(sys.argv) != 3:
        print('Usage: lab02.exe <input file> <output file>')
        return

    # if fail, return immediately
    f_in = openWithError(sys.argv[1], 'r')
    if f_in == None:
        return
    f_out = openWithError(sys.argv[2], 'w')
    if f_out == None:
        f_in.close()

    pathProblem = PathProblem(f_in)

    # must close file after return
    f_in.close()
    f_out.close()
    return


# https://stackoverflow.com/questions/4041238/why-use-def-main
if __name__ == '__main__':
    main()
