#!/usr/bin/env python3

from nbtschematic import SchematicFile

def main():
    # TODO: Training Logic Here
    schem = SchematicFile.load('../schematics/traininghills.schematic')
    print("The block at Y=%d, Z=%d, X=%d has block ID %d" % (10, 0, 0, schem.blocks[2, 3, 0]))
    print(len(schem.blocks))

if __name__ == '__main__':
    main()