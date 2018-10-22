# for GUI
import pygame
import GUIColor

import PathProblem


class GUIFindPath:
    def __init__(self, name_in, name_log):
        f_in = open(name_in, 'r')
        f_log = open(name_log, 'w')

        # doc bai toan tu file
        self.dataMap = PathProblem.DataMap(f_in, f_log)

        # tinh hop le cua bai toan
        self.valid = self.dataMap.checkValid()

        f_in.close()
        f_log.close()

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
        self.screen.fill(GUIColor.Color.data['Black'])

    # update screen with delay time
    def display(self):
        pygame.display.flip()
        self.clock.tick(5)

    # p is tuple (row, col)
    def drawPoint(self, p, color):
        pygame.draw.rect(
            self.screen, color,
            [(self.margin_size + self.p_size) * p[0] + self.margin_size,
             (self.margin_size + self.p_size) * p[1] + self.margin_size,
             self.p_size, self.p_size])

    def drawAStar(self):
        # bai toan khong hop le thi khong chay
        if not self.valid:
            return

        # draw o trong va vat can
        for row in range(self.dataMap.size):
            for col in range(self.dataMap.size):
                # mac dinh la o trong
                color = GUIColor.Color.data['White']

                # vat can
                if self.dataMap.arr[row][col] == '1':
                    color = GUIColor.Color.data['Gray']

                # to mau
                self.drawPoint((row, col), color)

        # draw SPoint, GPoint
        self.drawPoint(self.dataMap.SPoint, GUIColor.Color.data['Red'])
        self.drawPoint(self.dataMap.GPoint, GUIColor.Color.data['Orange'])

        self.display()

        # Keep window stay open
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
