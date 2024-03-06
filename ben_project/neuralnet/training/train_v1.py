from pathlib import Path

import torch
from torch import nn
from torch.utils import data

from neuralnet.models import SchematicLSTM
from neuralnet.util.utils import generate_slice_sequences
from schempy import Schematic


def train(schem: Schematic, token_to_index, index_to_token, output_name: str):

    num_tokens = len(schem.get_palette().keys())
    torch.set_default_device('cuda')
    features, labels = generate_slice_sequences(schem, token_to_index, index_to_token)

    print(len(features))
    for i in range(0, len(features)):
        print(features[i], labels[i])

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
    optimizer = torch.optim.SGD(model.parameters(), lr=0.0001)

    print("Commencing training...")

    epochs = 100
    loss = None
    for epoch in range(epochs):
        print(f'Epoch {epoch + 1}')
        for X, y in dataloader:
            y_hat = model(X)
            loss = loss_fn(y_hat, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch + 1} Finished: Loss = {loss.item():.4f}')


    print("Saving Model")
    #torch.save(model.state_dict(), f"neuralnet/models/state/{output_name}.pt")

