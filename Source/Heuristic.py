import math


def EuclidDistance(p, q):
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    return math.sqrt(dx * dx + dy * dy)


def MyHeuristic(p, q):
    # p = (2, 3), q = (7, 10)
    # di duong cheo it nhat  co the,
    # den khi chi con duong thang
    # (2, 3) -> (7, 8)
    cost_cheo = min(abs(q[0] - p[0]), abs(q[1] - p[1]))
    # chac chan heuristic chap nhan duoc
    return cost_cheo // 2