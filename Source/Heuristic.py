import math


def EuclidDistance(p, q):
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    return math.sqrt(dx * dx + dy * dy)
