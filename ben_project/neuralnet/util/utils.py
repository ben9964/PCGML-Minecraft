def generate_sequence(schem, token_to_index, index_to_token):
    sequence = []
    for x in range(0, schem.width):
        for y in range(schem.height - 1, -1, -1):
            for z in range(0, schem.length):
                block = schem.get_block(x, y, z)
                index = token_to_index[block.id]
                sequence.append(index)
    return sequence