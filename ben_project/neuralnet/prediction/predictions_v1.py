from pathlib import Path

import torch

from schempy import Schematic
from neuralnet.util.utils import generate_sequence


def predict(model, token_to_index, index_to_token):
    model.eval()

    seed_schem = Schematic.from_file(Path("seed_schems/seed.schem"))
    seed_sequence = torch.tensor(generate_sequence(seed_schem, token_to_index, index_to_token), dtype=torch.long)
    print("before")
    print(seed_sequence)

    hidden_state = (torch.zeros(model.num_layers, model.hidden_size),
                    torch.zeros(model.num_layers, model.hidden_size))

    for _ in range(10):
        output, hidden_state = model(seed_sequence, hidden_state)
        output = output.squeeze()  # Potentially remove extra dimension
        probabilities = torch.softmax(output, dim=-1)
        predicted_index = torch.multinomial(probabilities, num_samples=1)[0].item()
        seed_sequence = torch.cat((seed_sequence, torch.tensor([predicted_index])), dim=-1)

    print("after")
    print(seed_sequence)