import markov.train as tm
import markov.generate as gen

def main():
    schem = "training_2"
    #tm.train(schem)
    gen.generate(schem)

if __name__ == '__main__':
    main()