#!/usr/bin/env python3

from pathlib import Path

from ..schempy import Schematic

def train():
    # TODO: Training Logic Here
    path = Path('schematics/traininghills.schem')
    schem = Schematic.from_file(path)
    # Loop over all 


