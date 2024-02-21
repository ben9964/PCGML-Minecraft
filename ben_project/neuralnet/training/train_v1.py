from pathlib import Path

import torch
from torch import nn
from torch.utils import data

from neuralnet.models import SchematicLSTM
from neuralnet.util.utils import generate_sequence
from schempy import Schematic


def train(schem: Schematic, palette, output_name: str):
    token_to_index = {token: index for index, token in enumerate(palette)}
    index_to_token = {index: token for token, index in token_to_index.items()}

    torch.set_default_device('cuda')
    sequence = generate_sequence(schem, token_to_index, index_to_token)

    print("Generated Training Sequence")

    model = SchematicLSTM.of(len(palette))

    features = torch.tensor(sequence, dtype=torch.long)
    features = features[:-1]
    labels = torch.tensor(sequence[1:], dtype=torch.long)

    dataset = data.TensorDataset(features, labels)
    dataloader = data.DataLoader(dataset, batch_size=16, shuffle=True, generator=torch.Generator(device='cuda'))

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    print("Commencing training...")

    epochs = 3
    loss = None
    for epoch in range(epochs):
        print(f'Epoch {epoch + 1}')
        for X, y in dataloader:
            optimizer.zero_grad()
            hidden_state = (torch.zeros(model.num_layers, model.hidden_size),
                            torch.zeros(model.num_layers, model.hidden_size))
            y_hat, hidden_state = model(X, hidden_state)
            y_hat = y_hat.squeeze(-1)  # Reshape for CrossEntropyLoss
            loss = loss_fn(y_hat, y)
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch + 1} Finished: Loss = {loss.item():.4f}')


    print("Savind Model")
    torch.save(model.state_dict(), f"neuralnet/models/{output_name}.pt")

