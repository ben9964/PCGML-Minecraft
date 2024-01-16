#!/usr/bin/env python3

from pathlib import Path

from schempy import Schematic

def train():
    # TODO: Training Logic Here
    path = Path('schematics/traininghills.schem')
    schem = Schematic.from_file(path)
    dict = {}

    for i in range(0, schem.width):
        for j in range(0, schem.height):
            for k in range(0, schem.length):
                block = schem.get_block(i,j,k)
                # substring after minecraft:
                material = block.id[10:]
                if material in dict:
                    dict[material] += 1
                else:
                    dict[material] = 1
    print(dict["diamond_block"])


