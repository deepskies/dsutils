import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from torch.utils.data import Dataset, DataLoader

import dsutils as ds
# from dsutils.auto import train
from dsutils.auto import shape

class VAE(nn.Module):
    '''
    This network is defined recursively.
    |layers| ~ log_n(input_dim)

    output dim is bottleneck layer size

    The minimum number of layers needs to be 3 i think

    '''
    def __init__(self, input_dim, output_dim, config):
        super(VAE, self).__init__()
        layer_type = config['layer_type']
        self.classify = config.get('classify')

        if not self.classify:
            self.classify = False

        if layer_type == 'mlp':
            factor = config['factor']
            self.dims = shape.log_dims(input_dim, output_dim, factor=factor)
            self.enc = nn.ModuleList(shape.mlp_layers(self.dims))
            self.dec = nn.ModuleList(shape.mlp_layers(self.dims[::-1]))
        else:
            raise NotImplementedError("this layer type not supported yet")
        self.num_layers = len(self.dims)

    def single_direction(self, x, direction):
        # directions: encoding and decoding
        for i, layer in enumerate(direction):
            if i == self.num_layers - 1:
                if self.classify:
                    x = F.softmax(layer(x), dim=1)
                else:
                    x = F.relu(layer(x), dim=1)
                # break
            x = torch.tanh(layer(x))
        return x

    def forward(self, x):
        class_prediction = self.single_direction(x, self.enc)
        dec = self.single_direction(class_prediction, self.dec)
        return class_prediction, dec

    def __repr__(self):
        print(f'encoder: {self.enc}')
        print(f'decoder: {self.dec}')
        return 'network'
