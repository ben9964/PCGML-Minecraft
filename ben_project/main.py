import markov.training.train_v4 as tm
import markov.generation.generate_v4 as gen
import neuralnet.training.train_v1 as nt

def main():
    #tm.train("input_schems/medieval", "multi_key")
    #gen.generate("multi_key", "testwithseed")
    nt.train("input_schems/test/testseed2.schem", "testwith")

if __name__ == '__main__':
    main()