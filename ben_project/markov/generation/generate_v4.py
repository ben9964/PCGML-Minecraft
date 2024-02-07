import pickle
import random
from pathlib import Path

from schempy import Schematic, Block
from markov.training import key_functions as kf


def generate(pickle_id: str, output_name: str):
    directions = ["x-z-", "x-z+", "x+z-", "x+z+"]
    markovProbabilitiesAbove = pickle.load(open("markov/probabilities/" + pickle_id + "above_probabilities.pickle", "rb"))
    markovProbabilitiesBelow = pickle.load(
        open("markov/probabilities/" + pickle_id + "below_probabilities.pickle", "rb"))
    schem = Schematic(100, 50, 100)
    #schem = Schematic.from_file(Path("markov/output_schems/multi_key_generated.schem"))
    airWeightingTop = 1.0
    airWeightingBottom = 1.0

    for i in range(0, 10):
        print("Pass: " + str(i))
        for x in range(0, schem.width):
            for y in range(schem.height - 1, -1, -1):
                for z in range(0, schem.length):
                    if y <= schem.height/4:
                        probabilities = {}
                        for direction in directions:
                            key = kf.get_key_xyz(schem, x, y, z, direction)
                            if key in markovProbabilitiesBelow[direction].keys():
                                for key2 in markovProbabilitiesBelow[direction][key]:
                                    if key2 in probabilities.keys():
                                        if key2 == "minecraft:air":
                                            probabilities[key2] += (markovProbabilitiesBelow[direction][key][key2]*airWeightingBottom)
                                            #continue
                                        else:
                                            probabilities[key2] += markovProbabilitiesBelow[direction][key][key2]
                                    else:
                                        if key2 == "minecraft:air":
                                            probabilities[key2] = (markovProbabilitiesBelow[direction][key][key2]*airWeightingBottom)
                                            #continue
                                        else:
                                            probabilities[key2] = markovProbabilitiesBelow[direction][key][key2]

                        # If NO keys match
                        if len(probabilities) <= 0:
                            schem.set_block(x, y, z, Block("minecraft:stone"))
                            continue

                        normalized = {}
                        sumVal = 0
                        for key in probabilities.keys():
                            sumVal += probabilities[key]

                        for key in probabilities.keys():
                            normalized[key] = probabilities[key] / sumVal

                        randomSample = random.uniform(0, 1)
                        currValue = 0.0
                        for key in normalized:
                            if randomSample >= currValue and randomSample < currValue + normalized[key]:
                                schem.set_block(x, y, z, Block(key))
                                break
                            currValue += normalized[key]
                    else:
                        probabilities = {}
                        for direction in directions:
                            key = kf.get_key_xyz(schem, x, y, z, direction)
                            if key in markovProbabilitiesAbove[direction].keys():
                                for key2 in markovProbabilitiesAbove[direction][key]:
                                    if key2 in probabilities.keys():
                                        if key2 == "minecraft:air":
                                            probabilities[key2] += (markovProbabilitiesAbove[direction][key][key2] * airWeightingTop)
                                            #continue
                                        else:
                                            probabilities[key2] += markovProbabilitiesAbove[direction][key][key2]
                                    else:
                                        if key2 == "minecraft:air":
                                            probabilities[key2] = (markovProbabilitiesAbove[direction][key][key2] * airWeightingTop)
                                            #continue
                                        else:
                                            probabilities[key2] = markovProbabilitiesAbove[direction][key][key2]

                        # If NO keys match
                        if len(probabilities) <= 0:
                            schem.set_block(x, y, z, Block("minecraft:dirt"))
                            continue

                        normalized = {}
                        sumVal = 0
                        for key in probabilities.keys():
                            sumVal += probabilities[key]

                        for key in probabilities.keys():
                            normalized[key] = probabilities[key] / sumVal

                        randomSample = random.uniform(0, 1)
                        currValue = 0.0
                        for key in normalized:
                            if randomSample >= currValue and randomSample < currValue + normalized[key]:
                                schem.set_block(x, y, z, Block(key))
                                break
                            currValue += normalized[key]

    schem.save_to_file(Path("markov/output_schems/" + output_name + "_generated.schem"), 2)

