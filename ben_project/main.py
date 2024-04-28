from pathlib import Path

import markov.training.train_v4 as tm
import markov.generation.generate_v4 as gen
import neuralnet.training.train_v1 as nt
import neuralnet.training.train_v2 as ntv2
import neuralnet.prediction.predictions_v1 as np
from neuralnet.models import SchematicLSTM, SchematicLinear
from schempy import Schematic


def main():
    # This line executes the training script, it can be commented out to use an existing set of probabilities
    # The first argument is the path to the training schematics
    # the second argument is the name of the probabilities pickle file to output when finished
    tm.train("input_schems/medieval", "multi_key")
    # This executes the generation script with the first argument being the name of the probabilities pickle file
    # the second argument is the output name of the schematic
    # Example:
    # gen.generate("multi_key", "test") would use multi_key(above/below)_probabilities.pickle to generate a schematic
    # you can also specify a third boolean argument of whether to start with a blank or seed schematic for generation
    gen.generate("multi_key", "test")


    #The lines below are for the beginning of the neural network approach that is very barebones

    # schem, tokens = SchematicLinear.get_training_schem()
    # token_to_index = {token: index for index, token in enumerate(tokens)}
    # index_to_token = {index: token for token, index in token_to_index.items()}
    # print("Loaded Schematic")
    #nt.train(schem, token_to_index, index_to_token, "test_train_model_lstm")

    # np.predict(SchematicLinear.of(len(tokens)), token_to_index, index_to_token)

if __name__ == '__main__':
    main()