# Testing our custom heuristic

import sys

import Heuristic
import RandomProblem
import SolveProblem


def main():
    # auto random file if no input
    if len(sys.argv) != 3:
        RandomProblem.createRandomProblem('rand_in.txt', 8, 16)
        pf = SolveProblem.AStar('rand_in.txt', 'rand_log.txt')
        pf.writeSolution('rand_out.txt', Heuristic.MyHeuristic)
    else:
        pf = SolveProblem.AStar(sys.argv[1], 'log.txt')
        pf.writeSolution(sys.argv[2], Heuristic.MyHeuristic)


if __name__ == '__main__':
    main()