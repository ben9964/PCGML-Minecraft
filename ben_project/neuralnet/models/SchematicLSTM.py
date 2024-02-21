from pathlib import Path

from torch import nn

from schempy import Schematic


def get_training_schem():
    schem = Schematic.from_file(Path("input_schems/medieval/mountain.schem"))
    return schem, [block.id for block in schem.get_palette().keys()]

def of(num_tokens):
    embedding_dim = 32
    hidden_size = 64
    num_layers = 2
    return SchematicLSTM(num_tokens, embedding_dim, hidden_size, num_layers, num_tokens)

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