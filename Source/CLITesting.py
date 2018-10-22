import RandomProblem
import PathProblem


def main():
    RandomProblem.createRandomProblem('rand_in.txt', 8, 16)
    findPath = PathProblem.FindPath('rand_in.txt', 'rand_log.txt')
    findPath.writeSolution('rand_out.txt', findPath.AStar,
                           PathProblem.EuclidDistance)


if __name__ == '__main__':
    main()