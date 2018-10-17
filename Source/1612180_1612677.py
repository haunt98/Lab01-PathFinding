# for arguments
import sys

import math
import random


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
        for i in range(0, len(self.data)):
            if self.data[i].isSamePos(replacePoint):
                if self.data[i].cost > replacePoint.cost:
                    self.data[i].cost = replacePoint.cost
                    self.data[i].parent = replacePoint.parent
                break

    # return Point with lowest f()
    # f(n) = cost(n) + heuristic(n)
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

    # check if pathMap is correct size
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

    # point inside map and point not obstacle
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
    def __init__(self, f_in, f_log):
        # split for line to split to word
        size = int(f_in.readline())

        # startPoint
        startPointData = f_in.readline().split(',')
        x = int(startPointData[0])
        y = int(startPointData[1])
        self.startPoint = Point(x, y)

        # goalPoint
        goalPointData = f_in.readline().split(',')
        x = int(goalPointData[0])
        y = int(goalPointData[1])
        self.goalPoint = Point(x, y)

        self.pathMap = PathMap(f_in, size)

        # log file
        self.f_log = f_log

    # print what read from file again
    # include size, startPoint, goalPoint and pathMap
    def print(self):
        self.pathMap.printSize()
        print(self.startPoint.row, self.startPoint.col)
        print(self.goalPoint.row, self.goalPoint.col)
        self.pathMap.printMap()

    # check if data read from file is valid
    def isValid(self):
        # check if pathMap is correct size
        if not self.pathMap.isValid():
            self.f_log.write('pathMap is not valid')
            return False
        # check if start point and goal point is insize map
        # and is not obstacle
        if not self.pathMap.isMovablePoint(
                self.startPoint) or not self.pathMap.isMovablePoint(
                    self.goalPoint):
            self.f_log.write(
                'startPoint or goalPoint is not in map or is obstacle')
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
            # remove follow heuristic
            point = openList.remove(self.goalPoint)

            # found goal
            if point.isSamePos(self.goalPoint):
                return point

            # add current point to closeList
            closeList.add(point)

            for nextPoint in self.pathMap.nextMove(point):
                # nextPoint already close
                if closeList.exist(nextPoint):
                    continue

                # nextPoint not yet open
                if not openList.exist(nextPoint):
                    openList.add(nextPoint)
                # nextPoint exist in openList
                # replace if nextPoint has lower cost
                else:
                    openList.replace(nextPoint)

        # no solution found
        return None

    # Trace solution path follow from goalPoint
    # which parent of goalPoint
    # which parent of parent of goalPoint
    # ... whatever
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

    # write a solution to a file
    # -1 if no slution
    def writeSolution(self, f_out):
        goalPoint = self.solveAStar()
        if goalPoint == None:
            f_out.write('-1\n')
            return

        # cost to goal
        f_out.write(str(goalPoint.cost) + '\n')

        # path to goal
        for point in self.getSolutionPath(goalPoint):
            f_out.write('(' + str(point.row) + ',' + str(point.col) + ') ')
        f_out.write('\n')

        # create solutionMap
        solutionMap = []
        for row in self.pathMap.data:
            solutionMap.append(row)

        # write obstacle point
        for i in range(0, len(solutionMap)):
            for j in range(0, len(solutionMap[i])):
                if solutionMap[i][j] == '0':
                    solutionMap[i][j] = '-'
                elif solutionMap[i][j] == '1':
                    solutionMap[i][j] = 'o'

        # write solutionPath
        for point in self.getSolutionPath(goalPoint):
            solutionMap[point.row][point.col] = 'x'

        # write startPoint, goalPoint
        # because write solutionPath override startPoint, goalPoint
        solutionMap[self.startPoint.row][self.startPoint.col] = 'S'
        solutionMap[goalPoint.row][goalPoint.col] = 'G'

        # write to file
        for row in solutionMap:
            for col in row:
                f_out.write(col + ' ')
            f_out.write('\n')


class RandomPathProblem:
    def __init__(self, f_rand, maxSize):
        random.seed()

        # random size
        self.size = random.randrange(1, 1000) % maxSize + 1

        # random startPoint, goalPoint
        self.startPointRow = random.randrange(0, self.size)
        self.startPointCol = random.randrange(0, self.size)
        self.goalPointRow = random.randrange(0, self.size)
        self.goalPointCol = random.randrange(0, self.size)

        # random pathMap
        self.pathMap = []
        for i in range(0, self.size):
            row = []
            for j in range(0, self.size):
                row.append(random.randrange(0, 1000) % 2)
            self.pathMap.append(row)

        # write size to file
        f_rand.write(str(self.size) + '\n')

        # write startPoint, goalPoint to file
        f_rand.write(
            str(self.startPointRow) + ',' + str(self.startPointCol) + '\n')
        f_rand.write(
            str(self.goalPointRow) + ',' + str(self.goalPointCol) + '\n')

        # write pathMap to file
        for row in self.pathMap:
            for col in row:
                f_rand.write(str(col) + ' ')
            f_rand.write('\n')


def testSolvePathProblem(maxSize):
    f_rand = openWithError('rand.txt', 'w')
    if f_rand == None:
        return
    randomPathProblem = RandomPathProblem(f_rand, maxSize)
    f_rand.close()

    f_in = openWithError('rand.txt', 'r')
    if f_in == None:
        return
    f_out = openWithError('rand_out.txt', 'w')
    if f_out == None:
        f_in.close()
        return
    f_log = openWithError('rand_log.txt', 'w')
    if f_log == None:
        f_in.close()
        f_out.close()

    findingPathProblem = FindingPathProblem(f_in, f_log)
    findingPathProblem.writeSolution(f_out)

    f_in.close()
    f_out.close()
    f_log.close()


def solvePathProblem(file_input, file_output, file_log):
    # if fail, return immediately
    f_in = openWithError(file_input, 'r')
    if f_in == None:
        return
    f_out = openWithError(file_output, 'w')
    if f_out == None:
        f_in.close()
    # use log to store error when run program
    f_log = openWithError(file_log, 'w')
    if f_log == None:
        f_in.close()
        f_out.close()

    findingPathProblem = FindingPathProblem(f_in, f_log)
    findingPathProblem.writeSolution(f_out)

    # must close file after return
    f_in.close()
    f_out.close()
    f_log.close()


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
        print('Usage: 1612180_1612677.exe <input file> <output file>')
        return

    solvePathProblem(sys.argv[1], sys.argv[2], 'log.txt')
    testSolvePathProblem(8)

    return


# https://stackoverflow.com/questions/4041238/why-use-def-main
if __name__ == '__main__':
    main()