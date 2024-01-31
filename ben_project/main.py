import markov.training.train as tm
import markov.generation.generate as gen

def main():
    schem = "testhill"
    tm.train(schem)
    gen.generate(schem)

if __name__ == '__main__':
    main()