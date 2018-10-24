# for GUI
import pygame

# for PriorityQueue
import queue

import ReadProblem


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
        'Yellow': (250, 189, 47),
        'Dark Green': (121, 116, 14),
        'Dark Aqua': (66, 123, 88),
        'Dark Blue': (7, 102, 120),
        'Dark Red': (157, 0, 6)
    }


class GUIAStar:
    def __init__(self, name_in, name_log):
        # doc bai toan tu file
        self.dataMap = ReadProblem.DataMap(name_in, name_log)

        # kich thuoc cua cua so hien ra
        self.win_size = 512

        # margin la khoang cach giua cac o vuong
        self.margin_size = 4

        # kich thuoc cua o vuong
        self.p_size = (self.win_size - self.dataMap.size *
                       (self.margin_size + 1)) // self.dataMap.size

        # clock for delay update display
        self.clock = pygame.time.Clock()

        # tao window, title, background
        pygame.init()
        self.screen = pygame.display.set_mode([self.win_size, self.win_size])
        pygame.display.set_caption('Minh hoa A*')
        self.screen.fill(MyColor.data['Black'])

    # update screen with delay time
    def display(self):
        pygame.display.flip()
        self.clock.tick(5)

    # p is tuple (row, col)
    def drawPoint(self, p, color):
        pygame.draw.rect(
            self.screen, color,
            [(self.margin_size + self.p_size) * p[1] + self.margin_size,
             (self.margin_size + self.p_size) * p[0] + self.margin_size,
             self.p_size, self.p_size])

    # draw o trong va vat can
    def drawOTrongVatCan(self):
        for row in range(self.dataMap.size):
            for col in range(self.dataMap.size):
                # mac dinh la o trong
                color = MyColor.data['White']

                # vat can
                if self.dataMap.arr[row][col] == '1':
                    color = MyColor.data['Gray']

                # to mau
                self.drawPoint((row, col), color)

    # clone AStar.Solve
    def drawAStar(self, heuristic):
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

                    self.drawPoint(np, MyColor.data['Yellow'])

            self.display()

        return previousDict, costDict

    # clone getSolutionPath, include SPoint and GPoint
    def drawSolutionPath(self, previousDict, color):
        self.drawPoint(self.dataMap.GPoint, color)
        self.display()

        p = previousDict[self.dataMap.GPoint]
        # if p == None => SPoint == GPoint
        while p != None and p in previousDict and previousDict[p] != None:
            self.drawPoint(p, color)
            self.display()
            p = previousDict[p]

        self.drawPoint(self.dataMap.SPoint, color)
        self.display()

    def draw(self, heuristic):
        # bai toan khong hop le thi khong chay
        if not self.dataMap.valid:
            return

        self.drawOTrongVatCan()
        self.drawPoint(self.dataMap.SPoint, MyColor.data['Red'])
        self.drawPoint(self.dataMap.GPoint, MyColor.data['Dark Green'])
        self.display()

        previousDict, costDict = self.drawAStar(heuristic)
        # if have solution
        if self.dataMap.GPoint in previousDict:
            self.drawSolutionPath(previousDict, MyColor.data['Blue'])

        # Keep window stay open
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
