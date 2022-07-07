from Parser import Parser
import Simulate
import sys


def main():
    if len(sys.argv) != 2:
        print('usage: python main.py <filename>')
        sys.exit(1)
    n_p, n_a, tmax, events = Parser(sys.argv[1])
    Simulate.Simulate(n_p, n_a, tmax, events)

if __name__ == "__main__":
    main()
