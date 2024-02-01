#!/usr/bin/env python3
from schempy import Schematic


def get_key_xyz(schem: Schematic, x: int, y: int, z: int):
    westdown = " "
    southwestdown = " "
    southdown = " "
    down = " "

    if y < schem.height - 1:
        down = schem.get_block(x, y + 1, z).id
    if x > 0 and y < schem.height - 1:
        westdown = schem.get_block(x - 1, y + 1, z).id
    if z > 0 and y < schem.height - 1:
        southdown = schem.get_block(x, y + 1, z - 1).id
    if x > 0 and z > 0 and y < schem.height - 1:
        southwestdown = schem.get_block(x - 1, y + 1, z - 1).id

    key = get_key_xz(schem, x, y, z) + westdown + southwestdown + southdown + down
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


def get_key_xz(schem: Schematic, x: int, y: int, z: int):
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
    for key in markovCounts.keys():
        markovProbabilities[key] = {}

        sumVal = 0
        for key2 in markovCounts[key].keys():
            sumVal += markovCounts[key][key2]
        for key2 in markovCounts[key].keys():
            markovProbabilities[key][key2] = markovCounts[key][key2] / sumVal
    return markovProbabilities
