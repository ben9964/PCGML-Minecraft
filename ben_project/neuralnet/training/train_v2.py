from pathlib import Path

import torch
from torch import nn
from torch.utils import data

from neuralnet.models import SchematicLSTM, SchematicLinear
from neuralnet.util.utils import generate_slice_sequences
from schempy import Schematic


def train(schem: Schematic, token_to_index, index_to_token, output_name: str):

    num_tokens = len(schem.get_palette().keys())
    torch.set_default_device('cuda')
    features, labels = generate_slice_sequences(schem, token_to_index, index_to_token)

    print(token_to_index)

    features = torch.tensor(features).float()
    labels = torch.tensor(labels)
    labels = torch.nn.functional.one_hot(labels, num_classes=num_tokens)
    labels = labels.float()
    print(labels.shape)
    print(features.shape)

    print("Generated Training Sequence")

    model = SchematicLSTM.of(num_tokens)

    dataset = data.TensorDataset(features, labels)
    dataloader = data.DataLoader(dataset, batch_size=16, shuffle=True, generator=torch.Generator(device='cuda'))

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

    print("Commencing training...")

    epochs = 100
    loss = None
    state = None
    for epoch in range(epochs):
        print(f'Epoch {epoch + 1}')
        for X, Y in dataloader:
            if state is None:
                state = model.begin_state(batch_size=X.shape[0])
            # print(X.size(), Y.size(), state.size()) # 32x35, 32x35, 32x256
            y = Y.T.reshape(-1)
            # print(y.size()) # 35x32 -> 1120
            y_hat, state = model(X, state)
            # print(y_hat.size()) # 1120x28
            loss = loss_fn(y_hat, y.long())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch + 1} Finished: Loss = {loss.item():.4f}')


    print("Saving Model")
    torch.save(model.state_dict(), f"neuralnet/models/state/{output_name}.pt")

