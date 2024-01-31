#!/usr/bin/env python3
import pickle
from pathlib import Path

from schempy import Schematic
from markov.training import key_functions as kf

def train(schem_name: str):
    path = Path('input_schems/' + schem_name + '.schem')
    schem = Schematic.from_file(path)

    markovCounts = kf.get_counts_xyz(schem)
    markovProbabilities = kf.normalize(markovCounts)

    pickle.dump(markovProbabilities, open("markov/probabilities/" + schem_name + "_probabilities.pickle", "wb"))
