import markov.train as tm
import markov.generate as gen

def main():
    tm.train("flowers")
    gen.generate("flowers")

if __name__ == '__main__':
    main()