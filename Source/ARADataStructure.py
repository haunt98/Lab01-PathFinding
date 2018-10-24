import heapq


class ARAPriorityQueue:
    def __init__(self):
        # self.arr[i] is (prority, point_position)
        # self.arr[i][1] is point_position
        self.arr = []

    def empty(self):
        # empty list is False
        return not self.arr

    def add(self, priority, point_position):
        heapq.heappush(self.arr, (priority, point_position))

    def remove(self):
        return heapq.heappop(self.arr)[1]