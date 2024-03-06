import torch


def generate_sequence(schem, token_to_index, index_to_token):
    sequence = []
    for x in range(0, schem.width):
        for y in range(schem.height - 1, -1, -1):
            for z in range(0, schem.length):
                block = schem.get_block(x, y, z)
                index = token_to_index[block.id]
                sequence.append(index)
    return sequence


# input features are rows of [block at same pos in below slice, block at same pos in above slive, current slice height, prev block 1, prev block 2, prev block 3]
# label is the block at the position
def generate_slice_sequences(schem, token_to_index, index_to_token):
    features = []
    labels = []
    for y in range(0, schem.height):
        for z in range(0, schem.length):
            for x in range(0, schem.width):
                block = token_to_index[schem.get_block(x, y, z).id]
                below: int
                if y-1 < 0:
                    below = -1
                else:
                    below = token_to_index[schem.get_block(x, y-1, z).id]
                above: int
                if y+1 >= schem.height:
                    above = -1
                else:
                    above = token_to_index[schem.get_block(x, y+1, z).id]
                prev = get_prev_3_horizontal(schem, x, y, z)
                if None in prev:
                    continue
                features.append(
                    [
                        below,
                        above,
                        y,
                        token_to_index[prev[0]],
                        token_to_index[prev[1]],
                        token_to_index[prev[2]]
                    ]
                )
                labels.append(block)
    return features, labels

# Predicts in the x direction
def get_last_slice_features(schem, token_to_index):
    sequences = []
    for y in range(0, schem.height):
        maxX = schem.width - 1
        maxZ = schem.length - 1
        prev = get_prev_3_horizontal(schem, maxX+1, y, 0)
        #TODO: Make it recognise new generated slices below
        below = -1
        above = -1
        sequences.append(
            [
                below,
                above,
                y,
                token_to_index[prev[0]],
                token_to_index[prev[1]],
                token_to_index[prev[2]]
            ]
        )
    return sequences

def get_prev_3_horizontal(schem, x, y, z):
    prev = []
    tempx = x
    tempz = z
    for i in range(0, 3):
        tempz -= 1
        if tempz >= 0:
            prev.append(schem.get_block(tempx, y, tempz).id)
        elif tempx-1 >= 0:
            tempx -= 1
            tempz = schem.length-1
            prev.append(schem.get_block(tempx, y, tempz).id)
        else:
            prev.append(None)
    return prev

def get_above(schem, x, y, z):
    if y+1 >= schem.height:
        return -1
    return schem.get_block(x, y+1, z).id

def get_below(schem, x, y, z):
    if y-1 < 0:
        return -1
    return schem.get_block(x, y-1, z).id