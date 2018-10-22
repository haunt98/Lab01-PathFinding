import RandomProblem
import GUIDraw


def main():
    RandomProblem.createRandomProblem('rand_in.txt', 4, 8)
    g = GUIDraw.GUIFindPath('rand_in.txt', 'rand_log.txt')
    g.drawAStar()


if __name__ == '__main__':
    main()