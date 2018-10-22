import RandomProblem
import SolveProblem
import Heuristic


def main():
    RandomProblem.createRandomProblem('rand_in.txt', 8, 16)
    pf = SolveProblem.Pathfinding('rand_in.txt', 'rand_log.txt')
    pf.writeSolution('rand_out.txt', pf.AStar, Heuristic.EuclidDistance)


if __name__ == '__main__':
    main()