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
            for col in line.split():
                row.append(str(col))
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
        temp = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                (row, col + 1), (row + 1, col + 1), (row + 1, col),
                (row + 1, col - 1), (row, col - 1)]
        nlist = []

        # np is next point
        for np in temp:
            if self.isInside(np) and not self.isObstacle(np):
                nlist.append(np)

        return nlist