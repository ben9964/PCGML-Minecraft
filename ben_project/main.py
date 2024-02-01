import markov.training.train_v3 as tm
import markov.generation.generate_v3 as gen

def main():
    tm.train("input_schems/medieval", "medieval_split_v2_moreair")
    gen.generate("medieval_split_v2_moreair", "medieval_split_v2_moreair")

if __name__ == '__main__':
    main()