import markov.training.train_v2 as tm
import markov.generation.generate_v3 as gen

def main():
    #tm.train("input_schems/medieval", "medieval_v2")
    gen.generate("medieval_v2", "medieval_v2")

if __name__ == '__main__':
    main()