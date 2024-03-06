from pathlib import Path

import torch

from schempy import Schematic, Block
from neuralnet.util.utils import get_last_slice_features, get_prev_3_horizontal


def predict(model, token_to_index, index_to_token):
    model.eval()
    model.load_state_dict(torch.load(Path("neuralnet/models/state/smalltest_model_refined.pt")))

    seed_schem = Schematic.from_file(Path("seed_schems/seed.schem"))
    last_features = get_last_slice_features(seed_schem, token_to_index)
    seed_schem.reshape(seed_schem.width+1, seed_schem.height, seed_schem.length)

    for i in range(0, seed_schem.height):
        input_features = last_features[i]
        #below
        if i > 0:
            input_features[0] = token_to_index[seed_schem.get_block(seed_schem.width - 1, i - 1, 0).id]
        input_features = torch.tensor(input_features, dtype=torch.float)
        with torch.no_grad():
            out = model(input_features)
            class_index = out.argmax().item()
            seed_schem.set_block(seed_schem.width-1, i, 0, Block(index_to_token[class_index]))

    seed_schem.save_to_file(Path("neuralnet/output_schems/second_column.schem"), 2)

    print(token_to_index)
    print(index_to_token[model(torch.tensor([3, -1, 20, 3, 3, 3], dtype=torch.float)).argmax().item()])
