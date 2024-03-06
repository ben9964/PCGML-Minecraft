from pathlib import Path

import torch

from schempy import Schematic, Block
from neuralnet.util.utils import get_last_slice_features, get_prev_3_horizontal


def predict(model, token_to_index, index_to_token):
    model.eval()
    model.load_state_dict(torch.load(Path("neuralnet/models/state/test_train_model_lstm.pt")))

    seed_schem = Schematic.from_file(Path("seed_schems/small_seed.schem"))
    seed_schem.reshape(seed_schem.width+23, seed_schem.height, seed_schem.length)

    for y in range(0, seed_schem.height):
        for x in range(2, seed_schem.width):
            for z in range(0, seed_schem.length):
                seed_schem.set_block(x, y, z, Block("minecraft:air"))

    for y in range(0, seed_schem.height):
        for x in range(2, seed_schem.width):
            for z in range(0, seed_schem.length):
                prev = get_prev_3_horizontal(seed_schem, x, y, z)
                input_features = [-1, token_to_index[prev[0]], token_to_index[prev[1]], token_to_index[prev[2]]]
                #below
                if y > 0:
                    input_features[0] = token_to_index[seed_schem.get_block(x, y - 1, z).id]
                input_features = torch.tensor(input_features, dtype=torch.float)
                with torch.no_grad():
                    out = model(input_features)
                    class_index = out.argmax().item()
                    print(input_features)
                    print(index_to_token[class_index])
                    seed_schem.set_block(x, y, z, Block(index_to_token[class_index]))

    seed_schem.save_to_file(Path("neuralnet/output_schems/small.schem"), 2)

    print(token_to_index)
