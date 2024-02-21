from pathlib import Path

import torch
from torch import nn
from torch.utils import data

from schempy import Schematic


def train(schem_path: str, output_name: str):
    # Tokenization
    schem = Schematic.from_file(Path("input_schems/test/testseed2.schem"))
    tokens = [block.id for block in schem.get_palette().keys()]
    token_to_index = {token: index for index, token in enumerate(tokens)}
    index_to_token = {index: token for token, index in token_to_index.items()}

    # Feature and label creation
    sequence = []
    for x in range(0, schem.width):
        for y in range(schem.height - 1, -1, -1):
            for z in range(0, schem.length):
                block = schem.get_block(x, y, z)
                index = token_to_index[block.id]
                sequence.append(index)

    num_tokens = len(tokens)

    embedding_dim = 32
    hidden_size = 64
    num_layers = 2
    output_size = num_tokens

    model = SchematicLSTM(num_tokens, embedding_dim, hidden_size, num_layers, output_size)

    features = torch.tensor(sequence, dtype=torch.long)
    features = features[:-1]
    labels = torch.tensor(sequence[1:], dtype=torch.long)  # Labels are shifted by one
    print(features)
    print(labels)

    # Dataset and dataloader
    dataset = data.TensorDataset(features, labels)
    dataloader = data.DataLoader(dataset, batch_size=16, shuffle=True)  # Changed shuffle to True

    # Model, loss, optimizer
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    epochs = 10
    for epoch in range(epochs):
        for X, y in dataloader:
            optimizer.zero_grad()
            hidden_state = (torch.zeros(model.num_layers, model.hidden_size),
                            torch.zeros(model.num_layers, model.hidden_size))
            y_hat, hidden_state = model(X, hidden_state)
            y_hat = y_hat.squeeze(-1)  # Reshape for CrossEntropyLoss
            loss = loss_fn(y_hat, y)
            loss.backward()
            optimizer.step()

            if epoch % 10 == 0:
                print(f'Epoch {epoch + 1}: Loss = {loss.item():.4f}')

class SchematicLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size, num_layers, output_size):
        super().__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_size, num_layers)  # Input size now matches embedding_dim
        self.linear = nn.Linear(hidden_size, output_size)


    def forward(self, sequence, hidden_state):
        embeddings = self.embedding(sequence)  # Convert token indices to embeddings
        lstm_out, hidden_state = self.lstm(embeddings, hidden_state)
        predictions = self.linear(lstm_out)
        predictions = predictions.squeeze(-1)
        return predictions, hidden_state