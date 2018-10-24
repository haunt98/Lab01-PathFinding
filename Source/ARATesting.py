import Heuristic
import RandomProblem
import SolveProblem


def main():
    RandomProblem.createRandomProblem('rand_in.txt', 8, 16)
    pf = SolveProblem.ARA('rand_in.txt', 'rand_log.txt', 3,
                          Heuristic.EuclidDistance)
    pf.Solve()


if __name__ == '__main__':
    main()