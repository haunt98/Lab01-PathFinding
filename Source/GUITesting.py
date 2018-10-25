import sys

import RandomProblem
import Heuristic
import GUIDraw


def main():
    # auto random file if no input
    if len(sys.argv) != 2:
        RandomProblem.createRandomProblem('rand_in.txt', 12, 24)
        g = GUIDraw.GUIAStar('rand_in.txt', 'rand_log.txt')
        g.draw(Heuristic.EuclidDistance)
    else:
        g = GUIDraw.GUIAStar(sys.argv[1], 'GUI_log.txt')
        g.draw(Heuristic.EuclidDistance)


if __name__ == '__main__':
    main()