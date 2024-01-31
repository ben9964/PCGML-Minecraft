import pickle
import random
from pathlib import Path

from schempy import Schematic, Block
from markov.training import key_functions as kf


def generate(pickle_id: str):
    markovProbabilities = pickle.load(open("markov/probabilities/" + pickle_id + "_probabilities.pickle", "rb"))
    schem = Schematic(25, 25, 25)

    maxY = schem.height - 1
    for y in range(maxY, -1, -1):
        for x in range(0, schem.width):
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
                    if random.uniform(0, 1) > 0.5:
                        schem.set_block(x, y, z, Block("minecraft:air"))
                    else:
                        schem.set_block(x, y, z, Block("minecraft:stone"))

    schem.save_to_file(Path("markov/output_schems/" + pickle_id + "_generated.schem"), 2)

