import pandas


class DataHandler(object):  # Class for handling .csv file
    def __init__(self, **kwargs):
        """
        Path: path to the .csv file
        Df: DataFrame object
        """
        self.path = kwargs.get("path", None)
        self.df = pandas.read_csv(self.path, sep=";")

    def get_data(self):
        """
        :return: array with all data from the DataFrame
        """
        return self.df.values

