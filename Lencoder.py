"""
The Lencoder (Label encoder) module.

You can fit and update an encoder; transform and inverse transform your data.

At this point the encoders are going to be saved as pickle files. Improvements will be made.

emre95@gmail.com, 2019-03-29
"""
import pandas as pd
import pickle
from collections import OrderedDict


class Lencoder():
    """The Lencoder class."""

    def __init__(self):
        """Init method."""
        pass

    def update(self, data: pd.Series, encoder_path: str):
        """
        Update the given encoder with the given newcomer data.

        You can update your encoder to transform/inverse transform the new data.
        Don't worry, the updater will find the smallest numerical label.

        data            the newcomer data
        encoder_path    the encoder to be updated
        """
        newcomer_classes = set(data)
        with open(encoder_path, 'rb') as file:
            old_classes: dict = pickle.load(file)

        newcomer_classes.difference_update(set(old_classes.keys()))

        sorted_values = list(old_classes.values())

        for new_class in newcomer_classes:
            old_classes[new_class] = self._find_first_missing(
                sorted_values, 0, len(sorted_values) - 1)
            sorted_values.append(old_classes[new_class])

        with open(encoder_path, 'wb') as file:
            pickle.dump(old_classes, file)

    def fit(self, data: pd.Series, encoder_path: str):
        """
        Fit the encoder with data for the first time.

        Use this to fit your encoder for the first time. Don't use this
        if you are updating an old encoder with new data.

        data            the data to be fitted to encoder
        encoder_path    the path for the new encoder to be saved
        """
        newcomer_classes = set(data)
        encoder_dict = dict()

        for new_class, value in zip(newcomer_classes, range(len(newcomer_classes))):
            encoder_dict[new_class] = value

        with open(encoder_path, 'wb') as file:
            pickle.dump(encoder_dict, file)

    def transform(self, data: pd.Series, encoder_path: str):
        """Encode your data with the given encoder."""
        encoder_dict: dict = dict()
        transformed = list()

        with open(encoder_path, 'rb') as file:
            encoder_dict = pickle.load(file)

        for _, key in data.iteritems():
            transformed.append(encoder_dict[key])

        return transformed

    def inverse_transform(self, data: pd.Series, encoder_path: str):
        """Decode your data with the given encoder."""
        encoder_dict: dict = dict()
        inverse_transformed = list()

        with open(encoder_path, 'rb') as file:
            encoder_dict = pickle.load(file)

        inverted_encoder_dict: dict = dict(map(reversed, encoder_dict.items()))
        del encoder_dict

        for _, value in data.iteritems():
            inverse_transformed.append(inverted_encoder_dict[value])

        return inverse_transformed

    def _find_first_missing(self, array, start, end):
        """Credits to https://www.geeksforgeeks.org/find-the-first-missing-number/."""
        if (start > end):
            return end + 1

        if (start != array[start]):
            return start

        mid = int((start + end) / 2)

        if (array[mid] == mid):
            return self._find_first_missing(array,
                                            mid+1, end)

        return self._find_first_missing(array,
                                        start, mid)
