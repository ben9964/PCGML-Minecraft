#!/usr/bin/env python3
import pickle
from pathlib import Path

from schempy import Schematic
from markov.training import key_functions as kf
import time

def train(directory_name: str, output_name: str):
    directions = ["x-z-", "x-z+", "x+z-", "x+z+"]
    markovCountsAbove = {}  # Dictionary of the 7 blocks around the corner as keys
    markovCountsBelow = {}  # Dictionary of the 7 blocks around the corner as keys
    for filename in Path(directory_name).glob('*.schem'):
        path = Path(directory_name + "/" + filename.name)
        print("Training: " + filename.name)
        timeBeforeProcess = time.time()
        schem = Schematic.from_file(path)
        print("Loaded in: " + str(time.time() - timeBeforeProcess))
        timeBeforeProcess = time.time()
        for x in range(0, schem.width):
            for y in range(schem.height - 1, -1, -1):
                for z in range(0, schem.length):
                    for direction in directions:
                        key = kf.get_key_xyz(schem, x, y, z, direction)
                        block = schem.get_block(x, y, z).id
                        if y <= schem.height/4:
                            addCounts(markovCountsBelow, key, block, direction)
                        else:
                            addCounts(markovCountsAbove, key, block, direction)

        print("Finished in: " + str(time.time() - timeBeforeProcess))

    print("normalizing...")
    timeBeforeNormalize = time.time()
    markovProbabilities = kf.normalize(markovCountsAbove)
    print("Normalized in: " + str(time.time() - timeBeforeNormalize))

    print("dumping...")
    pickle.dump(markovProbabilities, open("markov/probabilities/" + output_name + "above_probabilities.pickle", "wb"))

    print("normalizing...")
    timeBeforeNormalize = time.time()
    markovProbabilities = kf.normalize(markovCountsBelow)
    print("Normalized in: " + str(time.time() - timeBeforeNormalize))

    print("dumping...")
    pickle.dump(markovProbabilities, open("markov/probabilities/" + output_name + "below_probabilities.pickle", "wb"))


def addCounts(markovCounts: dict, key: str, block : str, direction: str):
    if not direction in markovCounts.keys():
        markovCounts[direction] = {}
    if not key in markovCounts[direction].keys():
        markovCounts[direction][key] = {}
    if not block in markovCounts[direction][key].keys():
        markovCounts[direction][key][block] = 0
    markovCounts[direction][key][block] += 1.0
