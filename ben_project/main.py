from pathlib import Path

import markov.training.train_v4 as tm
import markov.generation.generate_v4 as gen
import neuralnet.training.train_v1 as nt
import neuralnet.prediction.predictions_v1 as np
from neuralnet.models import SchematicLSTM
from schempy import Schematic


def main():
    #tm.train("input_schems/medieval", "multi_key")
    #gen.generate("multi_key", "testwithseed")
    schem, tokens = SchematicLSTM.get_training_schem()
    print("Loaded Schematic")
    #nt.train(schem, tokens, "mountain_model")
    token_to_index = {token: index for index, token in enumerate(tokens)}
    index_to_token = {index: token for token, index in token_to_index.items()}
    np.predict(SchematicLSTM.of(len(tokens)), token_to_index, index_to_token)

if __name__ == '__main__':
    main()