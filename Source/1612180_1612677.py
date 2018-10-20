# for arguments
import sys

import math
import random

# for GUI
import pygame


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

    def calc_heruristic_euclid(self, goalPoint):
        return self.cost + self.EuclideanDistance(goalPoint)


# AStarList object for store Point
class AStarList:
    def __init__(self):
        self.data = []

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

    # return Point with lowest heuristic
    def remove(self, goalPoint):
        if self.isEmpty():
            return
        minIndex = 0
        for i in range(1, len(self.data)):
            if self.data[i].calc_heruristic_euclid(goalPoint) < self.data[
                    minIndex].calc_heruristic_euclid(goalPoint):
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
    # Luu size, startPoint, goalPoint and map data
    # map look like
    # 1 0 0
    # 0 1 0
    # 0 1 0
    # 1 is obstacle, 0 is not
    def __init__(self, f_in):
        # get size
        self.size = int(f_in.readline())

        # get startPoint
        startPointData = f_in.readline().split(',')
        x = int(startPointData[0])
        y = int(startPointData[1])
        self.startPoint = Point(x, y)

        # get goalPoint
        goalPointData = f_in.readline().split(',')
        x = int(goalPointData[0])
        y = int(goalPointData[1])
        self.goalPoint = Point(x, y)

        # get map data
        self.data = []
        for line in f_in:
            row = []
            for word in line.split():
                row.append(str(word))
            self.data.append(row)

    # check if map data is valid len row and len col
    def isValid(self):
        # chieu dai row va col phai = size
        if len(self.data) != self.size:
            return False
        for row in self.data:
            if len(row) != self.size:
                return False

        # startPoint va goalPoint phai trong map va di chuyen duoc
        if not self.isMovablePoint(self.startPoint) or not self.isMovablePoint(
                self.goalPoint):
            return False

        return True

    # return True if Point is in map
    def isPointInside(self, point):
        return point.row >= 0 and point.row < self.size and point.col >= 0 and point.col < self.size

    # return True if Point is obstacle
    def isObstaclePoint(self, point):
        return self.data[point.row][point.col] == '1'

    # point inside map and point not obstacle
    def isMovablePoint(self, point):
        return self.isPointInside(point) and not self.isObstaclePoint(point)

    # next move of p is Point from 1 to 8
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


class PathProblem:
    # get value from file
    def __init__(self, f_in, f_log):
        # include size, startPoint, goalPoint, map data
        self.pathMap = PathMap(f_in)

        # log file
        self.f_log = f_log

    # https://en.wikipedia.org/wiki/A*_search_algorithm
    def solveAStar(self):
        # check path map again for size
        if not self.pathMap.isValid():
            self.f_log.write('Data from file input is not valid\n')
            return None

        # init
        closeList = AStarList()
        openList = AStarList()
        openList.add(self.pathMap.startPoint)

        while not openList.isEmpty():
            # remove point which has lowest heuristic
            point = openList.remove(self.pathMap.goalPoint)

            # found goal
            if point.isSamePos(self.pathMap.goalPoint):
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

    # Trace solution path follow from finishPoint
    # which parent of finishPoint
    # which parent of parent of finishPoint
    # ... whatever
    def getSolutionPath(self, finishPoint):
        solutionPath = []
        if finishPoint == None:
            return
        p = finishPoint
        while p.parent != None:
            solutionPath.insert(0, p)
            p = p.parent
        solutionPath.insert(0, p)
        return solutionPath

    # write a solution to a file
    def writeSolution(self, f_out):
        # giai bang A*
        finishPoint = self.solveAStar()

        # khong co duong di
        if finishPoint == None:
            f_out.write('-1\n')
            return

        # cost
        f_out.write(str(finishPoint.cost) + '\n')

        # path
        for point in self.getSolutionPath(finishPoint):
            f_out.write('(' + str(point.row) + ',' + str(point.col) + ') ')
        f_out.write('\n')

        # create solutionMap
        solutionMap = []
        for row in self.pathMap.data:
            solutionMap.append(row)

        # '-' o trong
        # 'o' vat can
        for i in range(0, len(solutionMap)):
            for j in range(0, len(solutionMap[i])):
                if solutionMap[i][j] == '0':
                    solutionMap[i][j] = '-'
                elif solutionMap[i][j] == '1':
                    solutionMap[i][j] = 'o'

        # write solutionPath first
        for point in self.getSolutionPath(finishPoint):
            solutionMap[point.row][point.col] = 'x'

        # write startPoint, finishPoint later
        solutionMap[self.pathMap.startPoint.row][self.pathMap.startPoint.
                                                 col] = 'S'
        solutionMap[finishPoint.row][finishPoint.col] = 'G'

        # write map to file
        for row in solutionMap:
            for col in row:
                f_out.write(col + ' ')
            f_out.write('\n')


# thu vien dinh nghia cac mau sac
# https://github.com/morhetz/gruvbox
class MyColor:
    data = {
        'Aqua': (104, 157, 106),
        'Black': (40, 40, 40),
        'Blue': (69, 133, 136),
        'Gray': (146, 131, 116),
        'Green': (152, 151, 26),
        'Orange': (214, 93, 14),
        'Red': (204, 36, 29),
        'White': (251, 241, 198),
        'Yellow': (215, 153, 33),
        'Dark Green': (121, 116, 14),
        'Dark Aqua': (66, 123, 88),
        'Dark Blue': (7, 102, 120)
    }


# minh hoa A* bang GUI
class GUI_PathProblem:
    def __init__(self, f_in, f_log):
        # lay lai size, goalPoint, startPoint, map data
        self.pathMap = PathMap(f_in)

        # window size (kich thuoc cua cua so hien ra)
        self.WINDOW_WIDTH = 512
        self.WINDOW_HEIGHT = 512
        self.WINDOW_SIZE = [self.WINDOW_WIDTH, self.WINDOW_HEIGHT]

        # margin size (margin la khoang cach giua cac o vuong trong window)
        self.MARGIN_SIZE = 4

        # kich thuoc cua mot o vuong
        self.POINT_SIZE = (self.WINDOW_WIDTH - self.pathMap.size *
                           (self.MARGIN_SIZE + 1)) // self.pathMap.size

        # diem ket thuc de truy nguoc tim duong di
        self.finishPoint = None

        # clock for delay update display
        self.clock = pygame.time.Clock()

        pygame.init()

        # tao window, title, background
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption('Minh hoa A*')
        self.screen.fill(MyColor.data['Black'])

    # update screen with delay time
    def display(self):
        pygame.display.flip()
        self.clock.tick(2)

    def drawPoint(self, row, col, color):
        pygame.draw.rect(
            self.screen, color,
            [(self.MARGIN_SIZE + self.POINT_SIZE) * col + self.MARGIN_SIZE,
             (self.MARGIN_SIZE + self.POINT_SIZE) * row + self.MARGIN_SIZE,
             self.POINT_SIZE, self.POINT_SIZE])

    def drawStartGoal(self):
        self.drawPoint(self.pathMap.startPoint.row,
                       self.pathMap.startPoint.col, MyColor.data['Red'])
        self.drawPoint(self.pathMap.goalPoint.row, self.pathMap.goalPoint.col,
                       MyColor.data['Orange'])

    def drawSolutionPath(self, color):
        if self.finishPoint == None:
            return

        p = self.finishPoint
        while p.parent != None:
            self.drawPoint(p.row, p.col, color)
            self.display()
            p = p.parent
        self.drawPoint(p.row, p.col, color)
        self.display()

    def drawAStar(self):
        # draw o trong va vat can
        for row in range(self.pathMap.size):
            for col in range(self.pathMap.size):
                # mac dinh la o trong
                color = MyColor.data['White']

                # vat can
                if self.pathMap.data[row][col] == '1':
                    color = MyColor.data['Gray']

                # to mau o vuong
                self.drawPoint(row, col, color)

        # draw startPoint, goalPoint
        self.drawStartGoal()

        # update lai screen sau khi ve
        self.display()

        # minh hoa A*
        if self.pathMap.isValid():
            # init list
            closeList = AStarList()
            openList = AStarList()
            openList.add(self.pathMap.startPoint)

            while not openList.isEmpty():
                # lay diem gan goalPoint nhat theo heuristic
                point = openList.remove(self.pathMap.goalPoint)

                # found goal
                if point.isSamePos(self.pathMap.goalPoint):
                    self.finishPoint = point
                    self.drawSolutionPath(MyColor.data['Yellow'])
                    break
                else:
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

                for p in openList.data:
                    self.drawPoint(p.row, p.col, MyColor.data['Aqua'])
                self.drawStartGoal()
                self.display()

                for p in closeList.data:
                    self.drawPoint(p.row, p.col, MyColor.data['Dark Blue'])
                self.drawStartGoal()
                self.display()

        # Keep window stay open
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


class RandomPathProblem:
    def __init__(self, f_rand):
        random.seed()

        # random size
        self.size = random.randrange(8, 16)

        # random startPoint, goalPoint
        self.startPointRow = random.randrange(0, self.size)
        self.startPointCol = random.randrange(0, self.size)
        self.goalPointRow = random.randrange(0, self.size)
        self.goalPointCol = random.randrange(0, self.size)

        # random mapData
        self.mapData = []
        for i in range(0, self.size):
            row = []
            for j in range(0, self.size):
                row.append(random.randrange(0, 1000) % 2)
            self.mapData.append(row)

        # write size to file
        f_rand.write(str(self.size) + '\n')

        # write startPoint, goalPoint to file
        f_rand.write(
            str(self.startPointRow) + ',' + str(self.startPointCol) + '\n')
        f_rand.write(
            str(self.goalPointRow) + ',' + str(self.goalPointCol) + '\n')

        # write mapData to file
        for row in self.mapData:
            for col in row:
                f_rand.write(str(col) + ' ')
            f_rand.write('\n')


def testSolveCmd():
    f_rand = openWithError('rand_in.txt', 'w')
    if f_rand == None:
        return
    randomPathProblem = RandomPathProblem(f_rand)
    f_rand.close()

    f_in = openWithError('rand_in.txt', 'r')
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

    pathProblem = PathProblem(f_in, f_log)
    pathProblem.writeSolution(f_out)

    f_in.close()
    f_out.close()
    f_log.close()


def solveCmd(file_input, file_output, file_log):
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

    # read problem from file
    pathProblem = PathProblem(f_in, f_log)

    # write solution to file
    pathProblem.writeSolution(f_out)

    f_in.close()
    f_out.close()
    f_log.close()


def solveGUI(file_input, file_log):
    # if fail, return immediately
    f_in = openWithError(file_input, 'r')
    if f_in == None:
        return
    # use log to store error when run program
    f_log = openWithError(file_log, 'w')
    if f_log == None:
        f_in.close()

    # minh hoa solution bang GUI
    gui = GUI_PathProblem(f_in, f_log)
    gui.drawAStar()

    f_in.close()
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

    solveGUI(sys.argv[1], 'log.txt')
    #solveCmd(sys.argv[1], sys.argv[2], 'log.txt')
    #testSolveCmd()

    return


if __name__ == '__main__':
    main()