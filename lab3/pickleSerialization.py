import pickle


class PickleSerializer:

    def serialize(self, obj, file):
        """
........Encode obj to binary row using pickle write it into file.
........"""

        pickle.dump(obj, file)

    def deserialize(self, file):
        """
........Decode from binary row to Python-object using pickle.
........"""

        return pickle.load(file)
