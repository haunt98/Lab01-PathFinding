# for arguments
import sys

import math


# Point object to show where in the map
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print(self):
        print(self.x, self.y)

    def EuclideanDistance(self, p):
        return math.sqrt((p.x - self.x) * (p.x - self.x) +
                         (p.y - self.y) * (p.y - self.y))


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
        self.startPoint.print()
        self.goalPoint.print()

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
    pathProblem.print()

    # must close file after return
    f_in.close()
    f_out.close()
    return


# https://stackoverflow.com/questions/4041238/why-use-def-main
if __name__ == '__main__':
    main()
