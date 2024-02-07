#!/usr/bin/env python3
from schempy import Schematic


def get_key_xyz(schem: Schematic, x: int, y: int, z: int, direction: str = "x-z-"):
    xydir = " "
    xyzdir = " "
    yzdir = " "
    ydir = " "
    match direction:
        case "x-z-":
            if y < schem.height - 1:
                ydir = schem.get_block(x, y + 1, z).id
            if x > 0 and y < schem.height - 1:
                xydir = schem.get_block(x - 1, y + 1, z).id
            if z > 0 and y < schem.height - 1:
                yzdir = schem.get_block(x, y + 1, z - 1).id
            if x > 0 and z > 0 and y < schem.height - 1:
                xyzdir = schem.get_block(x - 1, y + 1, z - 1).id

        case "x-z+":
            if y < schem.height - 1:
                ydir = schem.get_block(x, y + 1, z).id
            if x > 0 and y < schem.height - 1:
                xydir = schem.get_block(x - 1, y + 1, z).id
            if z < schem.length - 1 and y < schem.height - 1:
                yzdir = schem.get_block(x, y + 1, z + 1).id
            if x > 0 and z < schem.length - 1 and y < schem.height - 1:
                xyzdir = schem.get_block(x - 1, y + 1, z + 1).id

        case "x+z-":
            if y < schem.height - 1:
                ydir = schem.get_block(x, y + 1, z).id
            if x < schem.width - 1 and y < schem.height - 1:
                xydir = schem.get_block(x + 1, y + 1, z).id
            if z > 0 and y < schem.height - 1:
                yzdir = schem.get_block(x, y + 1, z - 1).id
            if x < schem.width - 1 and z > 0 and y < schem.height - 1:
                xyzdir = schem.get_block(x + 1, y + 1, z - 1).id

        case "x+z+":
            if y < schem.height - 1:
                ydir = schem.get_block(x, y + 1, z).id
            if x < schem.width - 1 and y < schem.height - 1:
                xydir = schem.get_block(x + 1, y + 1, z).id
            if z < schem.length - 1 and y < schem.height - 1:
                yzdir = schem.get_block(x, y + 1, z + 1).id
            if x < schem.width - 1 and z < schem.length - 1 and y < schem.height - 1:
                xyzdir = schem.get_block(x + 1, y + 1, z + 1).id

    key = get_key_xz(schem, x, y, z, direction) + xydir + xyzdir + yzdir + ydir
    return key

def get_key_xyz_up(schem: Schematic, x: int, y: int, z: int):
    westdown = " "
    southwestdown = " "
    southdown = " "
    down = " "

    if y > 0:
        down = schem.get_block(x, y - 1, z).id
    if x > 0 and y > 0:
        westdown = schem.get_block(x - 1, y - 1, z).id
    if z > 0 and y > 0:
        southdown = schem.get_block(x, y - 1, z - 1).id
    if x > 0 and z > 0 and y > 0:
        southwestdown = schem.get_block(x - 1, y - 1, z - 1).id

    key = get_key_xz(schem, x, y, z) + westdown + southwestdown + southdown + down
    return key


def get_key_xz(schem: Schematic, x: int, y: int, z: int, direction: str = "x-z-"):
    xdir = " "
    xzdir = " "
    zdir = " "
    match direction:
        case "x-z-":
            if x > 0:
                xdir = schem.get_block(x - 1, y, z).id
            if z > 0:
                zdir = schem.get_block(x, y, z - 1).id
            if x > 0 and z > 0:
                xzdir = schem.get_block(x - 1, y, z - 1).id

        case "x-z+":
            if x > 0:
                xdir = schem.get_block(x - 1, y, z).id
            if z < schem.length - 1:
                zdir = schem.get_block(x, y, z + 1).id
            if x > 0 and z < schem.length - 1:
                xzdir = schem.get_block(x - 1, y, z + 1).id

        case "x+z-":
            if x < schem.width - 1:
                xdir = schem.get_block(x + 1, y, z).id
            if z > 0:
                zdir = schem.get_block(x, y, z - 1).id
            if x < schem.width - 1 and z > 0:
                xzdir = schem.get_block(x + 1, y, z - 1).id

        case "x+z+":
            if x < schem.width - 1:
                xdir = schem.get_block(x + 1, y, z).id
            if z < schem.length - 1:
                zdir = schem.get_block(x, y, z + 1).id
            if x < schem.width - 1 and z < schem.length - 1:
                xzdir = schem.get_block(x + 1, y, z + 1).id

    key = xdir + xzdir + zdir
    return key

def get_counts_xyz_up(schem: Schematic, markovCounts=None):
    if markovCounts is None:
        markovCounts = {}
    for y in range(0, schem.height):
        for x in range(0, schem.width):
            for z in range(0, schem.length):
                key = get_key_xyz_up(schem, x, y, z)

                block = schem.get_block(x, y, z).id
                if not key in markovCounts.keys():
                    markovCounts[key] = {}
                if not block in markovCounts[key].keys():
                    markovCounts[key][block] = 0
                if schem.get_block(x, y, z).id == "minecraft:air":
                    markovCounts[key][block] += 0.1
                else:
                    markovCounts[key][block] += 1.0
    return markovCounts

def get_counts_xyz(schem: Schematic, markovCounts=None):
    if markovCounts is None:
        markovCounts = {}
    for x in range(0, schem.width):
        for y in range(schem.height - 1, -1, -1):
            for z in range(0, schem.length):
                key = get_key_xyz(schem, x, y, z)

                block = schem.get_block(x, y, z).id
                if not key in markovCounts.keys():
                    markovCounts[key] = {}
                if not block in markovCounts[key].keys():
                    markovCounts[key][block] = 0
                if schem.get_block(x, y, z).id == "minecraft:air":
                    markovCounts[key][block] += 0.5
                else:
                    markovCounts[key][block] += 1.0
    return markovCounts


def get_counts_xz(schem: Schematic, markovCounts=None):
    if markovCounts is None:
        markovCounts = {}
    maxy = schem.height - 1
    for y in range(maxy, -1, -1):
        for x in range(0, schem.width):
            for z in range(0, schem.length):
                west = " "
                southwest = " "
                south = " "

                if x > 0:
                    west = schem.get_block(x - 1, y, z).id
                if z > 0:
                    south = schem.get_block(x, y, z - 1).id
                if x > 0 and z > 0:
                    southwest = schem.get_block(x - 1, y, z - 1).id

                key = west + southwest + south

                if not key in markovCounts.keys():
                    markovCounts[key] = {}
                if not schem.get_block(x, y, z).id in markovCounts[key].keys():
                    markovCounts[key][schem.get_block(x, y, z).id] = 0
                markovCounts[key][schem.get_block(x, y, z).id] += 1.0

    return markovCounts


def normalize(markovCounts: dict):
    markovProbabilities = {}
    for direction in markovCounts.keys():
        for key in markovCounts[direction].keys():
            if not direction in markovProbabilities.keys():
                markovProbabilities[direction] = {}
            markovProbabilities[direction][key] = {}

            sumVal = 0
            for key2 in markovCounts[direction][key].keys():
                sumVal += markovCounts[direction][key][key2]
            for key2 in markovCounts[direction][key].keys():
                markovProbabilities[direction][key][key2] = markovCounts[direction][key][key2] / sumVal
    return markovProbabilities
