# for PriorityQueue
import queue

import ReadProblem

# for ARA
import ARAQueue

# for inf
import math

# the code below is a mess
# only God understand
# but God left


# only need map, cost of goal and path
# to write solution to file
def writeSolutionToFile(name_out, dataMap, costGoal, path, noSolution=False):
    f_out = open(name_out, 'w')
    if noSolution:
        f_out.write('-1\n')
        f_out.close()
        return

    # write cost
    f_out.write(str(costGoal) + '\n')

    # write path, include SPoint and GPoint
    f_out.write('(' + str(dataMap.SPoint[0]) + ',' + str(dataMap.SPoint[1]) +
                ') ')
    for p in path:
        f_out.write('(' + str(p[0]) + ',' + str(p[1]) + ') ')
    f_out.write('(' + str(dataMap.GPoint[0]) + ',' + str(dataMap.GPoint[1]) +
                ')\n')

    # write map
    arr = []
    for row in dataMap.arr:
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

    if dataMap.SPoint == dataMap.GPoint:
        arr[dataMap.SPoint[0]][dataMap.SPoint[1]] = 'S/G'
    else:
        arr[dataMap.SPoint[0]][dataMap.SPoint[1]] = 'S'
        arr[dataMap.GPoint[0]][dataMap.GPoint[1]] = 'G'

    for row in arr:
        for col in row:
            f_out.write(col + ' ')
        f_out.write('\n')

    f_out.close()


class AStar:
    def __init__(self, name_in, name_log):
        # doc bai toan tu file
        self.dataMap = ReadProblem.DataMap(name_in, name_log)

    # https://www.redblobgames.com/pathfinding/a-star/implementation.html
    # heuristic la mot ham truyen vao
    # tra ve previousDict, costDict
    def Solve(self, heuristic):
        # bai toan khong hop le thi khong chay
        # tra ve 2 empty dict
        if not self.dataMap.valid:
            return {}, {}

        # init with SPoint
        # costDict store cost of point we have so far
        # previousDict store previous of point we have so far
        costDict = {self.dataMap.SPoint: 0}
        previousDict = {self.dataMap.SPoint: None}

        # PriorityQueue with heuristic
        # PriorityQueue put tuple (priority, point position)
        openList = queue.PriorityQueue()
        openList.put((heuristic(self.dataMap.SPoint, self.dataMap.GPoint),
                      self.dataMap.SPoint))

        while not openList.empty():
            # cur is tuple (priority, point position)
            # cur[1] is point position
            cur = openList.get()

            # found goal
            if cur[1] == self.dataMap.GPoint:
                break

            # np is next point
            for np in self.dataMap.nextList(cur[1]):
                # every single move cost 1
                np_cost = costDict[cur[1]] + 1
                # previous of np is cur[1]
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
        # if p == None => SPoint == GPoint
        while p != None and previousDict[p] != None:
            path.insert(0, p)
            p = previousDict[p]

        return path

    # algo, heuristic la mot ham truyen vao
    def writeSolution(self, name_out, heuristic):
        #f_out = open(name_out, 'w')

        previousDict, costDict = self.Solve(heuristic)
        if self.dataMap.GPoint not in previousDict:
            #f_out.write('-1\n')
            #f_out.close()
            writeSolutionToFile(name_out, None, None, None, noSolution=True)
            return

        costGoal = costDict[self.dataMap.GPoint]
        path = self.getSolutionPath(previousDict)
        writeSolutionToFile(name_out, self.dataMap, costGoal, path)