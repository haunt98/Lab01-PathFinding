# for arguments
import sys

import PathProblem
import Heuristic


def main():
    if len(sys.argv) != 3:
        print('Usage: 1612180_1612677.exe <input file> <output file>')
        return

    findPath = PathProblem.FindPath(sys.argv[1], 'log.txt')
    findPath.writeSolution(sys.argv[2], findPath.AStar,
                           Heuristic.EuclidDistance)


if __name__ == '__main__':
    main()