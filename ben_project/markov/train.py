#!/usr/bin/env python3
import pickle
from pathlib import Path

from schempy import Schematic

def train(schem_name: str):
    # TODO: Training Logic Here
    path = Path('input_schems/' + schem_name + '.schem')
    schem = Schematic.from_file(path)

    markovCounts = {} # Dictionary of the 7 blocks around the corner as keys
    for x in range(0, schem.width):
        maxY = schem.height-1
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
                    west = schem.get_block(x-1,y,z).id
                if z > 0:
                    south = schem.get_block(x,y,z-1).id
                if x > 0 and z > 0:
                    southwest = schem.get_block(x-1,y,z-1).id
                if y < maxY:
                    down = schem.get_block(x,y+1,z).id
                if x > 0 and y < maxY:
                    westdown = schem.get_block(x-1,y+1,z).id
                if z > 0 and y < maxY:
                    southdown = schem.get_block(x,y+1,z-1).id
                if x > 0 and z > 0 and y < maxY:
                    southwestdown = schem.get_block(x-1,y+1,z-1).id

                key = west+southwest+south+westdown+southwestdown+southdown+down

                if not key in markovCounts.keys():
                    markovCounts[key] = {}
                if not schem.get_block(x,y,z).id in markovCounts[key].keys():
                    markovCounts[key][schem.get_block(x,y,z).id] = 0
                markovCounts[key][schem.get_block(x,y,z).id] += 1.0

    # Normalize markov counts
    markovProbabilities = {}
    for key in markovCounts.keys():
        markovProbabilities[key] = {}

        sumVal = 0
        for key2 in markovCounts[key].keys():
            sumVal += markovCounts[key][key2]
        for key2 in markovCounts[key].keys():
            markovProbabilities[key][key2] = markovCounts[key][key2] / sumVal

    pickle.dump(markovProbabilities, open("markov/probabilities/" + schem_name + "_probabilities.pickle", "wb"))
