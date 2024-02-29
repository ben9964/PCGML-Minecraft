from pathlib import Path

import torch
from torch import nn

from schempy import Schematic


def get_training_schem():
    schem = Schematic.from_file(Path("input_schems/test/smalltest.schem"))
    return schem, [block.id for block in schem.get_palette().keys()]

def of(num_tokens):
    inputs = 6
    return SchematicLSTM(num_inputs=inputs, num_outputs=num_tokens)

class SchematicLSTM(nn.Module):
    def __init__(self, num_inputs, num_outputs):
        super().__init__()
        # self.num_layers = num_layers
        # self.hidden_size = hidden_size
        self.num_inputs = num_inputs

        # self.lstm = nn.LSTM(num_tokens, hidden_size, num_layers)
        self.linear = nn.Linear(num_inputs, num_outputs)
        torch.nn.init.normal_(self.linear.weight, std=0.01)
        torch.nn.init.zeros_(self.linear.bias)


    def forward(self, features):
        features = features.view(-1, self.num_inputs)
        out = self.linear(features)
        predictions = torch.nn.functional.softmax(out, dim=-1)
        return predictions