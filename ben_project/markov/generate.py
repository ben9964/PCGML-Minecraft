import pickle
import random
from pathlib import Path

from schempy import Schematic, Block


def generate(schem_name: str):
    markovProbabilities = pickle.load(open("markov/probabilities/" + schem_name + "_probabilities.pickle", "rb"))
    schem = Schematic(25, 25, 25)

    for x in range(0, schem.width):
        maxY = schem.height - 1
        for y in range(maxY, -1, -1):
            for z in range(0, schem.length):
                west = " "
                southwest = " "
                south = " "
                westdown = " "
                southwestdown = " "
                southdown = " "
                down = " "

                if x > 0:
                    west = schem.get_block(x - 1, y, z).id
                if z > 0:
                    south = schem.get_block(x, y, z - 1).id
                if x > 0 and z > 0:
                    southwest = schem.get_block(x - 1, y, z - 1).id
                if y > 0:
                    down = schem.get_block(x, y - 1, z).id
                if x > 0 and y < maxY:
                    westdown = schem.get_block(x - 1, y + 1, z).id
                if z > 0 and y < maxY:
                    southdown = schem.get_block(x, y + 1, z - 1).id
                if x > 0 and z > 0 and y < maxY:
                    southwestdown = schem.get_block(x - 1, y + 1, z - 1).id

                key = west + southwest + south + westdown + southwestdown + southdown + down

                if key in markovProbabilities.keys():

                    randomSample = random.uniform(0, 1)
                    currValue = 0.0
                    for key2 in markovProbabilities[key]:
                        if randomSample >= currValue and randomSample < currValue + markovProbabilities[key][key2]:
                            schem.set_block(x, y, z, Block(key2))
                            break
                        currValue += markovProbabilities[key][key2]
                else:
                    #if random.uniform(0, 1) > 0.5:
                    schem.set_block(x, y, z, Block("minecraft:air"))
                    #else:
                        #schem.set_block(x, y, z, Block("minecraft:stone"))

    schem.save_to_file(Path("markov/output_schems/" + schem_name + "_generated.schem"), 2)

