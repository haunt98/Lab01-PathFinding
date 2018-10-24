import RandomProblem
import Heuristic
import GUIDraw


def main():
    RandomProblem.createRandomProblem('rand_in.txt', 12, 24)
    g = GUIDraw.GUIAStar('rand_in.txt', 'rand_log.txt')
    g.draw(Heuristic.EuclidDistance)


if __name__ == '__main__':
    main()