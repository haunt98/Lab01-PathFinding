import heapq


class ARAPriorityQueue:
    def __init__(self):
        self.data = []

    def add(self, priority, data):
        heapq.heappush(self.data, (priority, data))

    def remove(self):
        heapq.heappop(self.data)

    def min(self):
        if len(self.data) > 0:
            return self.data[0]
