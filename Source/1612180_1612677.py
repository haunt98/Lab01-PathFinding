# TODO write test, more test !!

# for arguments
import sys

import math


# Point object to show where in the map
# also cost and parent
class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.parent = None
        self.cost = 0

    def EuclideanDistance(self, point):
        return math.sqrt((point.row - self.row) * (point.row - self.row) +
                         (point.col - self.col) * (point.col - self.col))

    def isSamePos(self, point):
        return self.row == point.row and self.col == point.col

    def print(self):
        print(self.row, self.col, self.cost)

    # f(n) = cost(n) + heuristic(n)
    def calc_f(self, goalPoint):
        return self.cost + self.EuclideanDistance(goalPoint)


# AStarList object for store Point
# use f(n) = cost(n) + heuristic(n)
class AStarList:
    def __init__(self):
        self.data = []

    def print(self):
        for i in self.data:
            i.print()

    def isEmpty(self):
        # empty sequences are False
        return not self.data

    def add(self, newPoint):
        self.data.append(newPoint)

    # only replace if replacePoint has lower cost()
    def replace(self, replacePoint):
        for point in self.data:
            if point.isSamePos(replacePoint):
                if point.cost > replacePoint.cost:
                    point.cost = replacePoint.cost
                    point.parent = replacePoint.parent
                break

    # return Point with lowest f()
    def remove(self, goalPoint):
        if self.isEmpty():
            return
        minIndex = 0
        for i in range(1, len(self.data)):
            if self.data[i].calc_f(goalPoint) < self.data[minIndex].calc_f(
                    goalPoint):
                minIndex = i
        return self.data.pop(minIndex)

    # return True if findPoint exist
    # otherwise return False
    def exist(self, findPoint):
        for point in self.data:
            if point.isSamePos(findPoint):
                return True
        return False


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
                row.append(str(word))
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

    # return True if Point is in map
    # otherwise return False
    def isValidPoint(self, point):
        return point.row >= 0 and point.row < self.size and point.col >= 0 and point.col < self.size

    # return True if Point is obstacle
    # otherwise return False
    def isObstaclePoint(self, point):
        return self.data[point.row][point.col] == '1'

    def isMovablePoint(self, point):
        return self.isValidPoint(point) and not self.isObstaclePoint(point)

    # next move of p is Point from 1 to 8
    # valid move if next Point is in map and not obstacle
    # return list Point object
    # 1 2 3
    # 8 p 4
    # 7 6 5
    def nextMove(self, point):
        nextPointS = []
        # 1 2 3
        if self.isMovablePoint(Point(point.row - 1, point.col - 1)):
            nextPoint = Point(point.row - 1, point.col - 1)
            nextPoint.parent = point
            nextPoint.cost = point.cost + 1
            nextPointS.append(nextPoint)
        if self.isMovablePoint(Point(point.row - 1, point.col)):
            nextPoint = Point(point.row - 1, point.col)
            nextPoint.parent = point
            nextPoint.cost = point.cost + 1
            nextPointS.append(nextPoint)
        if self.isMovablePoint(Point(point.row - 1, point.col + 1)):
            nextPoint = Point(point.row - 1, point.col + 1)
            nextPoint.parent = point
            nextPoint.cost = point.cost + 1
            nextPointS.append(nextPoint)
        # 4
        if self.isMovablePoint(Point(point.row, point.col + 1)):
            nextPoint = Point(point.row, point.col + 1)
            nextPoint.parent = point
            nextPoint.cost = point.cost + 1
            nextPointS.append(nextPoint)
        # 5 6 7
        if self.isMovablePoint(Point(point.row + 1, point.col + 1)):
            nextPoint = Point(point.row + 1, point.col + 1)
            nextPoint.parent = point
            nextPoint.cost = point.cost + 1
            nextPointS.append(nextPoint)
        if self.isMovablePoint(Point(point.row + 1, point.col)):
            nextPoint = Point(point.row + 1, point.col)
            nextPoint.parent = point
            nextPoint.cost = point.cost + 1
            nextPointS.append(nextPoint)
        if self.isMovablePoint(Point(point.row + 1, point.col - 1)):
            nextPoint = Point(point.row + 1, point.col - 1)
            nextPoint.parent = point
            nextPoint.cost = point.cost + 1
            nextPointS.append(nextPoint)
        # 8
        if self.isMovablePoint(Point(point.row, point.col - 1)):
            nextPoint = Point(point.row, point.col - 1)
            nextPoint.parent = point
            nextPoint.cost = point.cost + 1
            nextPointS.append(nextPoint)
        return nextPointS

    def printNextMove(self, point):
        for move in self.nextMove(point):
            move.print()


class FindingPathProblem:
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

    def isValid(self):
        if not self.pathMap.isValid():
            return False
        if not self.pathMap.isObstaclePoint(
                self.startPoint) or not self.pathMap.isObstaclePoint(
                    self.goalPoint):
            return False
        return True

    # https://en.wikipedia.org/wiki/A*_search_algorithm
    # assume heuristic(n) is consistent
    # otherwise, must rediscover point in closeList
    def solveAStar(self):
        # check path map again for size
        if not self.isValid():
            return None

        # init closeList and openList
        closeList = AStarList()
        openList = AStarList()
        openList.add(self.startPoint)

        while not openList.isEmpty():
            point = openList.remove(self.goalPoint)

            # found goal
            if point.isSamePos(self.goalPoint):
                return point

            # move point from openList to closeList
            openList.remove(point)
            closeList.add(point)

            for nextPoint in self.pathMap.nextMove(point):
                # nextPoint already close
                if closeList.exist(nextPoint):
                    continue
                # nextPoint not yet open
                elif not openList.exist(nextPoint):
                    openList.add(nextPoint)
                # nextPoint exist in openList
                # replace if nextPoint has lower cost
                else:
                    openList.replace(nextPoint)

        # no solution found
        return None

    def getSolutionPath(self, goalPoint):
        solutionPath = []
        if goalPoint == None:
            return
        p = goalPoint
        while p.parent != None:
            solutionPath.insert(0, p)
            p = p.parent
        solutionPath.insert(0, p)
        return solutionPath

    def solution(self, f):
        goalPoint = self.solveAStar()
        if goalPoint == None:
            f.write('-1\n')
            return
        # cost to goal
        f.write(str(goalPoint.cost) + '\n')

        # path to goal
        for point in self.getSolutionPath(goalPoint):
            f.write('(' + str(point.row) + ',' + str(point.col) + ') ')
        f.write('\n')

        # create solution map
        solutionMap = []
        for row in self.pathMap.data:
            solutionMap.append(row)
        for row in solutionMap:
            for col in row:
                if col == 0:
                    col = '-'
                elif col == 1:
                    col = 'o'
        solutionMap[self.startPoint.row][self.startPoint.col] = 'S'
        solutionMap[goalPoint.row][goalPoint.col] = 'G'
        for point in self.getSolutionPath(goalPoint):
            solutionMap[point.row][point.col] = 'x'
        for row in solutionMap:
            for col in row:
                f.write(col + ' ')
            f.write('\n')


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

    findingPathProblem = FindingPathProblem(f_in)
    findingPathProblem.solution(f_out)

    # must close file after return
    f_in.close()
    f_out.close()
    return


# https://stackoverflow.com/questions/4041238/why-use-def-main
if __name__ == '__main__':
    main()
