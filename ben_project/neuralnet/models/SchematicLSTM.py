from pathlib import Path

import torch
from torch import nn

from schempy import Schematic


def get_training_schem():
    schem = Schematic.from_file(Path("input_schems/test/testtrain.schem"))
    return schem, [block.id for block in schem.get_palette().keys()]

def of(num_tokens):
    inputs = 4
    hidden_size = 32
    return SchematicLSTM(input_size=inputs, output_size=num_tokens, hidden_size=hidden_size)

class SchematicLSTM(nn.Module):
    def __init__(self, input_size, output_size, hidden_size):
        super().__init__()
        self.output_size = output_size
        self.input_size = input_size
        self.hidden_size = hidden_size

        self.rnn = nn.RNN(output_size, hidden_size)
        self.linear = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, inputs, state):
        X = torch.nn.functional.one_hot(inputs.T.long(), self.output_size)
        X = X.to(torch.float32)
        Y, state = self.rnn(X, state)
        # print(X.size()) # 35x32x28
        # print(Y.size()) # 35x32x256
        # print(state.size()) # 32x256
        Y1 = Y.reshape((-1, Y.shape[-1]))
        # print(Y1.size()) # 1120x256
        out = self.linear(Y1)
        # print(out.size()) # 1120x28
        return out, state

    def begin_state(self, batch_size=1):
        state = torch.zeros((self.rnn.num_layers, batch_size, self.hidden_size))
        return state
