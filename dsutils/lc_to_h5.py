import os

import pandas as pd
import numpy as np
import h5py

class IO:
    def __init__(self, id_col='object_id'):
        """
        * Loads light curve data
        * Creates the h5 file
        *

        """
        self.id_col = id_col

        self.df = pd.read_csv('../../cosmoNODE/demos/data/training_set.csv')
        self.meta = pd.read_csv('../../cosmoNODE/demos/data/training_set_metadata.csv')

        # main dataset h5 file
        self.f = h5py.File("lc.hdf5", 'w')

    def process(self):
        """
        * Creates the h5 groups
        * Puts light curve data in them
        *
        """
        # df = self.lcs.df
        # meta = self.lcs.meta
        df = self.df
        meta = self.meta

        groups = df.groupby(self.id_col)

        X = self.f.create_group('X')
        Y = self.f.create_group('Y')


        for i, group in enumerate(groups):
            group_id = group[0]
            group_data = group[1]
            group_label = meta.iloc[i]

            data_path = 'X' + str(group_id)
            X.create_dataset(str(group_id), data=group_data)
            Y.create_dataset(str(group_id), data=group_label)

        self.f.close()