import os
import pickle
import json
import sys
import yaml
from inspect import signature
import configparser


class Serialize:

    """
    Strategy class for selecting serialization type
    """
    _serializer = None

    def __init__(self):
        """
        constructor, init strategy for setting type of serialization.
        Serializer type is written in special file cfg
        """
        config = configparser.RawConfigParser()
        config.read('config.cfg')
        cls = config.get('SerializationSettings', 'serialize')
        self._serializer = sys.modules["serializers"].__dict__.get(cls)

    def save(self, filePath, table):
        """
        call selected serializer.save
        """
        return self._serializer.save(filePath, table)

    def load(self, filePath):
        """
        call selected serializer.load
        """
        return self._serializer.load(filePath)


class PickleSerialize:

    """
    Serialize database with pickle module
    """

    @staticmethod
    def save(filePath, table):
        """
        serialize to file :filePath list :table
        """
        with open("./tables/pickle/" + filePath + ".pickle", "wb") as f:
            pickle.dump(table, f)

    @staticmethod
    def load(filePath):
        """
        load data from file :filePath and return as list. If file doesn't
        exist, return empty list
        """
        if not os.path.isfile("./tables/pickle/" + filePath + ".pickle"):
            return []
        with open("./tables/pickle/" + filePath + ".pickle", "rb") as f:
            res = pickle.load(f)
            return [] if not isinstance(res, list) else res


class JsonSerialize:

    """
    Serialize database with json module
    """

    @staticmethod
    def save(filePath, table):
        """
        serialize to file :filePath list :table
        """
        with open("./tables/json/" + filePath + ".json", "w") as f:
            ls = []
            for i in table:
                data = JsonSerialize._prepareSave(i.__dict__)
                className = i.__class__.__name__
                ls.append([data, className])
            json.dump(ls, f)

    @staticmethod
    def _prepareSave(obj):
        """
        create a dictionary from objects. If object contains another object,
        recursively and return dict
        """
        res = {}
        for key, value in obj.items():
            if type(value) is str or type(value) is int:
                res[key] = value
            else:
                res[key] = [value.__dict__, value.__class__.__name__]
        return res

    @staticmethod
    def load(filePath):
        """
        load data from file :filePath and return as list. If file doesn't
        exist, return empty list
        """
        if not os.path.isfile("./tables/json/" + filePath + ".json"):
            return []
        res = []
        with open("./tables/json/" + filePath + ".json", "r") as f:
            for item in json.load(f):
                res.append(JsonSerialize._prepareLoad(item[0], item[1]))
        return res

    @staticmethod
    def _prepareLoad(data, className):
        """
        create an instance from dict and return it
        """
        attrs = {}
        for key, value in data.items():
            if type(value) is list:
                attrs[key] = JsonSerialize._prepareLoad(value[0], value[1])
            else:
                attrs[key] = value
        obj = JsonSerialize._getInstance(className)
        obj.initTable(attrs)
        return obj

    @staticmethod
    def _getInstance(cls):
        """
        create an instance of class and init its params
        """
        import models
        sig = signature(getattr(models.__dict__.get(cls), "__init__"))
        if len(sig.parameters) == 2:
            obj = models.__dict__.get(cls)("")
        else:
            obj = models.__dict__.get(cls)(models.Book(""), models.Author(""))
        return obj


class YamlSerialize:

    """
    Serialize database with yaml module
    """

    @staticmethod
    def save(filePath, table):
        """
        serialize to file :filePath list :table
        """
        with open("./tables/yaml/" + filePath + ".yaml", "w") as f:
            yaml.dump(table, f)

    @staticmethod
    def load(filePath):
        """
        load data from file :filePath and return as list. If file doesn't
        exist, return empty list
        """
        if not os.path.isfile("./tables/yaml/" + filePath + ".yaml"):
            return []
        with open("./tables/yaml/" + filePath + ".yaml", "r") as f:
            res = yaml.load(f)
            return [] if not isinstance(res, list) else res
