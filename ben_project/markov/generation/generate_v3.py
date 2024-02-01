import pickle
import random
from pathlib import Path

from schempy import Schematic, Block
from markov.training import key_functions as kf


def generate(pickle_id: str, output_name: str):
    markovProbabilities = pickle.load(open("markov/probabilities/" + pickle_id + "_probabilities.pickle", "rb"))
    schem = Schematic(25, 25, 25)

    blockPalette = []
    for key in markovProbabilities.keys():
        for key2 in markovProbabilities[key].keys():
            if not key2 in blockPalette:
                blockPalette.append(key2)

    maxY = schem.height - 1
    for x in range(0, schem.width):
        for y in range(maxY, -1, -1):
            for z in range(0, schem.length):
                key = kf.get_key_xyz(schem, x, y, z)

                if key in markovProbabilities.keys():
                    randomSample = random.uniform(0, 1)
                    currValue = 0.0
                    for key2 in markovProbabilities[key]:
                        if randomSample >= currValue and randomSample < currValue + markovProbabilities[key][key2]:
                            schem.set_block(x, y, z, Block(key2))
                            break
                        currValue += markovProbabilities[key][key2]
                else:
                    if y <= maxY/2:
                        schem.set_block(x, y, z, Block("minecraft:stone"))
                    else:
                        schem.set_block(x, y, z, Block("minecraft:air"))

    schem.save_to_file(Path("markov/output_schems/" + output_name + "_generated.schem"), 2)

