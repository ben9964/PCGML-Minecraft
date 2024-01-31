#!/usr/bin/env python3
import pickle
from pathlib import Path

from schempy import Schematic
from markov.training import key_functions as kf

def train(directory_name: str, output_name: str):
    markovCounts = {}  # Dictionary of the 7 blocks around the corner as keys
    for filename in Path(directory_name).glob('*.schem'):
        path = Path('input_schems/' + filename.name)
        print("Training: " + filename.name)
        schem = Schematic.from_file(path)
        markovCounts = kf.get_counts_xyz(schem, markovCounts)

    print("normalizing...")
    print(markovCounts)
    markovProbabilities = kf.normalize(markovCounts)

    # go through probabilities and weight air less than everything else
    for key in markovProbabilities.keys():
        for key2 in markovProbabilities[key].keys():
            if key2 == "minecraft:air":
                markovProbabilities[key][key2] = markovProbabilities[key][key2] * 0.01

    print("dumping...")
    print(markovProbabilities)
    pickle.dump(markovProbabilities, open("markov/probabilities/" + output_name + "_probabilities.pickle", "wb"))
