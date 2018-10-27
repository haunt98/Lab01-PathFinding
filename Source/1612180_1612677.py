# for arguments
import sys

import SolveProblem
import Heuristic


def main():
    if len(sys.argv) != 3:
        print('Usage: 1612180_1612677.exe <input file> <output file>')
        return

    pf = SolveProblem.AStar(sys.argv[1], 'log.txt')
    pf.writeSolution(sys.argv[2], Heuristic.EuclidDistance)


if __name__ == '__main__':
    main()