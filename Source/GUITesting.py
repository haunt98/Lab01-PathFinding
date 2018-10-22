import RandomProblem
import Heuristic
import GUIDraw


def main():
    RandomProblem.createRandomProblem('rand_in.txt', 8, 16)
    g = GUIDraw.GUIFindPath('rand_in.txt', 'rand_log.txt')
    g.draw(Heuristic.EuclidDistance)


if __name__ == '__main__':
    main()