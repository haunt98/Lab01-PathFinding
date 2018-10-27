import Heuristic
import RandomProblem
import SolveProblem


def main():
    RandomProblem.createRandomProblem('rand_in.txt', 8, 16)
    pf = SolveProblem.AStar('rand_in.txt', 'rand_log.txt')
    pf.writeSolution('rand_out.txt', Heuristic.EuclidDistance)


if __name__ == '__main__':
    main()