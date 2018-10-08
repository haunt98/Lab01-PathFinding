# for arguments
import sys

import math


# Point object to show where in the map
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def EuclideanDistance(self, p):
        return math.sqrt((p.x - self.x) * (p.x - self.x) +
                         (p.y - self.y) * (p.y - self.y))

    def isSame(self, point):
        return self.x == point.x and self.y == point.y


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
        print(self.point.x, self.point.y, self.cost)


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


class PathProblem:
    # get value from file
    # size
    # start_x start_y
    # goal_x goal_y
    # ...
    def __init__(self, f):
        # split for line to split to word
        self.size = int(f.readline())

        startPointData = f.readline().split()
        x = int(startPointData[0])
        y = int(startPointData[1])
        self.startPoint = Point(x, y)

        goalPointData = f.readline().split()
        x = int(goalPointData[0])
        y = int(goalPointData[1])
        self.goalPoint = Point(x, y)

        self.pathMap = []
        for line in f:
            row = []
            for word in line.split():
                row.append(int(word))
            self.pathMap.append(row)

    def print(self):
        print(self.size)
        print(self.startPoint.x, self.startPoint.y)
        print(self.goalPoint.x, self.goalPoint.y)

        for row in self.pathMap:
            for num in row:
                print(num, end=' ')
            # print() itself will print new line
            print()


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
