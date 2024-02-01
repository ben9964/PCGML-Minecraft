#!/usr/bin/env python3
import pickle
from pathlib import Path

from schempy import Schematic
from markov.training import key_functions as kf
import time

def train(directory_name: str, output_name: str):
    markovCounts = {}  # Dictionary of the 7 blocks around the corner as keys
    for filename in Path(directory_name).glob('*.schem'):
        path = Path(directory_name + "/" + filename.name)
        print("Training: " + filename.name)
        timeBeforeProcess = time.time()
        schem = Schematic.from_file(path)
        print("Loaded in: " + str(time.time() - timeBeforeProcess))
        timeBeforeProcess = time.time()
        markovCounts = kf.get_counts_xyz(schem, markovCounts)
        print("Finished in: " + str(time.time() - timeBeforeProcess))

    print("normalizing...")
    timeBeforeNormalize = time.time()
    markovProbabilities = kf.normalize(markovCounts)
    print("Normalized in: " + str(time.time() - timeBeforeNormalize))

    print("dumping...")
    pickle.dump(markovProbabilities, open("markov/probabilities/" + output_name + "_probabilities.pickle", "wb"))
