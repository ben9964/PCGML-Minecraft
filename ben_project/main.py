import markov.training.train_v4 as tm
import markov.generation.generate_v4 as gen

def main():
    #tm.train("input_schems/medieval", "multi_key")
    gen.generate("multi_key", "multi_key_10_pass_large")

if __name__ == '__main__':
    main()