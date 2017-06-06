from io import StringIO

import yaml

from serializers import JsonSerialize

import json


class JsonStream(StringIO):
    def read(self):
        return super().getvalue()


class YamlStream(StringIO):
    def read(self):
        return super().getvalue()


def jsonSerializeToStream(data):
    ls = []
    for i in data:
        ls.append([
            JsonSerialize._prepareSave(i.__dict__),
            i.__class__.__name__
        ])
    save_stream = JsonStream()
    json.dump(ls, save_stream)
    return save_stream, ls


def yamlSerializeToStream(data):
    stream = YamlStream()
    yaml.dump(data, stream, Dumper=yaml.Dumper)
    return stream
