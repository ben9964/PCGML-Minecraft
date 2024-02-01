import pickle
import random
from pathlib import Path

from schempy import Schematic, Block
from markov.training import key_functions as kf


def generate(pickle_id: str, output_name: str):
    markovProbabilitiesAbove = pickle.load(open("markov/probabilities/" + pickle_id + "above_probabilities.pickle", "rb"))
    markovProbabilitiesBelow = pickle.load(
        open("markov/probabilities/" + pickle_id + "below_probabilities.pickle", "rb"))
    schem = Schematic(100, 50, 100)

    for x in range(0, schem.width):
        for y in range(schem.height - 1, -1, -1):
            for z in range(0, schem.length):
                key = kf.get_key_xyz(schem, x, y, z)

                if y <= schem.height/4:
                    if key in markovProbabilitiesBelow.keys():
                        randomSample = random.uniform(0, 1)
                        currValue = 0.0
                        for key2 in markovProbabilitiesBelow[key]:
                            if randomSample >= currValue and randomSample < currValue + markovProbabilitiesBelow[key][key2]:
                                schem.set_block(x, y, z, Block(key2))
                                break
                            currValue += markovProbabilitiesBelow[key][key2]
                    else:
                        schem.set_block(x, y, z, Block("minecraft:stone"))
                else:
                    if key in markovProbabilitiesAbove.keys():
                        randomSample = random.uniform(0, 1)
                        currValue = 0.0
                        for key2 in markovProbabilitiesAbove[key]:
                            if randomSample >= currValue and randomSample < currValue + markovProbabilitiesAbove[key][key2]:
                                schem.set_block(x, y, z, Block(key2))
                                break
                            currValue += markovProbabilitiesAbove[key][key2]
                    else:
                        if random.uniform(0, 1) < 0.5:
                            schem.set_block(x, y, z, Block("minecraft:air"))
                        else:
                            schem.set_block(x, y, z, Block("minecraft:dirt"))

    schem.save_to_file(Path("markov/output_schems/" + output_name + "_generated.schem"), 2)

