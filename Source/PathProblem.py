import math

# for PriorityQueue
import queue


class DataMap:
    # Luu size, SPoint, GPoint, arr
    def __init__(self, f_in, f_log):
        self.size = int(f_in.readline())

        # Lay vi tri SPoint, GPoint
        p_str = f_in.readline().split(',')
        self.SPoint = (int(p_str[0]), int(p_str[1]))
        p_str = f_in.readline().split(',')
        self.GPoint = (int(p_str[0]), int(p_str[1]))

        # Lay vi tri vat can va o trong vao mang 2 chieu
        self.arr = []
        for line in f_in:
            row = []
            for word in line.split():
                row.append(str(word))
            self.arr.append(row)

        # Viet log khi doc file bi loi
        self.f_log = f_log

    # Kiem tra file input co hop le hay khong
    def checkValid(self):
        valid = True

        if len(self.arr) != self.size:
            self.f_log.write('number of row != size\n')
            valid = False
        for i in range(len(self.arr)):
            if len(self.arr[i]) != self.size:
                self.f_log.write('len of row ' + i + ' != size\n')
                valid = False

        if not self.isInside(self.SPoint):
            self.f_log.write('SPoint not inside map\n')
            valid = False

        if self.isObstacle(self.SPoint):
            self.f_log.write('SPoint is obstacle\n')
            valid = False

        if not self.isInside(self.GPoint):
            self.f_log.write('GPoint not inside map\n')
            valid = False

        if self.isObstacle(self.GPoint):
            self.f_log.write('GPoint is obstacle\n')
            valid = False

        return valid

    def isInside(self, p):
        if p[0] >= 0 and p[0] < self.size and p[1] >= 0 and p[1] < self.size:
            return True
        return False

    # kiem tra vat can
    def isObstacle(self, p):
        if self.arr[p[0]][p[1]] == '1':
            return True
        return False

    # tra ve cac diem ben canh p
    # 1 2 3
    # 8 p 4
    # 7 6 5
    # p = (row, col)
    def nextList(self, p):
        row = p[0]
        col = p[1]
        temp = [(row - 1, col - 1), (row - 1, col), (row - 1, col),
                (row, col + 1), (row + 1, col + 1), (row + 1, col),
                (row + 1, col - 1), (row, col - 1)]
        nlist = []

        # np is next point
        for np in temp:
            if self.isInside(np) and not self.isObstacle(np):
                nlist.append(np)

        return nlist


def EuclidDistance(p, q):
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    return math.floor(math.sqrt(dx * dx + dy * dy))


def samePosition(p, q):
    return p[0] == q[0] and p[1] == q[1]


class FindPath:
    def __init__(self, name_in, name_log):
        f_in = open(name_in, 'r')
        f_log = open(name_log, 'w')

        # doc bai toan tu file
        self.dataMap = DataMap(f_in, f_log)

        # tinh hop le cua bai toan
        self.valid = self.dataMap.checkValid()

        f_in.close()
        f_log.close()

    # https://www.redblobgames.com/pathfinding/a-star/implementation.html
    # heuristic la mot ham truyen vao
    # tra ve previousDict, costDict
    def AStar(self, heuristic):
        # bai toan khong hop le thi khong chay
        # tra ve 2 empty dict
        if self.valid == False:
            return {}, {}

        # init with SPoint
        # costDict store cost of point we have so far
        # previousDict store previous of point we have so far
        costDict = {self.dataMap.SPoint: 0}
        previousDict = {self.dataMap.SPoint: None}

        # PriorityQueue with heuristic
        # PriorityQueue put tuple (priority, point position)
        openList = queue.PriorityQueue()
        openList.put((0, self.dataMap.SPoint))

        while not openList.empty():
            cur = openList.get()

            # cur is tuple (priority, point position)
            # cur[1] is point position
            if samePosition(cur[1], self.dataMap.GPoint):
                break

            # np is next point
            for np in self.dataMap.nextList(cur[1]):
                np_cost = costDict[cur[1]] + 1
                np_previous = cur[1]

                # next point is new point => add
                # next point has lower cost => replace
                if np not in costDict or np_cost < costDict[np]:
                    costDict[np] = np_cost
                    previousDict[np] = np_previous

                    np_priority = np_cost + heuristic(np, self.dataMap.GPoint)
                    openList.put((np_priority, np))

        return previousDict, costDict

    # path is point between SPoint and GPoint
    # not include SPoint and GPoint
    def getSolutionPath(self, previousDict):
        path = []

        p = previousDict[self.dataMap.GPoint]
        while previousDict[p] != None:
            path.insert(0, p)
            p = previousDict[p]

        return path

    # algo, heuristic la mot ham truyen vao
    def writeSolution(self, name_out, algo, heuristic):
        f_out = open(name_out, 'w')

        previousDict, costDict = algo(heuristic)
        if self.dataMap.GPoint not in previousDict:
            f_out.write('-1\n')
            f_out.close()
            return

        # write cost
        f_out.write(str(costDict[self.dataMap.GPoint]) + '\n')

        # write path, include SPoint and GPoint
        f_out.write('(' + str(self.dataMap.SPoint[0]) + ',' +
                    str(self.dataMap.SPoint[1]) + ') ')
        path = self.getSolutionPath(previousDict)
        for p in path:
            f_out.write('(' + str(p[0]) + ',' + str(p[1]) + ') ')
        f_out.write('(' + str(self.dataMap.GPoint[0]) + ',' +
                    str(self.dataMap.GPoint[1]) + ')\n')

        # write map
        arr = []
        for row in self.dataMap.arr:
            arr.append(row)

        # 'S' SPoint
        # 'G' GPoint
        # '-' o trong
        # 'o' vat can
        # 'x' duong di
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if arr[i][j] == '0':
                    arr[i][j] = '-'
                elif arr[i][j] == '1':
                    arr[i][j] = 'o'
        for p in path:
            arr[p[0]][p[1]] = 'x'
        arr[self.dataMap.SPoint[0]][self.dataMap.SPoint[1]] = 'S'
        arr[self.dataMap.GPoint[0]][self.dataMap.GPoint[1]] = 'G'

        for row in arr:
            for word in row:
                f_out.write(word + ' ')
            f_out.write('\n')

        f_out.close()
