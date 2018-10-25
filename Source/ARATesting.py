import sys

import Heuristic
import RandomProblem
import SolveProblem


def main():
    # auto random file if no input
    if len(sys.argv) != 3:
        RandomProblem.createRandomProblem('rand_in.txt', 8, 16)
        pf = SolveProblem.ARA('rand_in.txt', 'rand_log.txt', 3,
                              Heuristic.EuclidDistance, 0.05)
        pf.writeSolution('rand_out.txt')
    else:
        pf = SolveProblem.ARA(sys.argv[1], 'ARA_log.txt', 3,
                              Heuristic.EuclidDistance, 0.05)
        pf.writeSolution(sys.argv[2])


if __name__ == '__main__':
    main()