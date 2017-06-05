import json
import modelController


class NoteEncoder(json.JSONEncoder):

    """
....Extension for json.JSONEncoder class which can encode
    objects of type Note.
    """

    def default(self, obj):
        """
        Extension for json.JSONEncoder.default function with adding
        ability to encode objects of type modelController.
        """

        if isinstance(obj, modelController.ModelController):
            listObj = []
            for i in obj.notes:
                row = {}
                row['name'] = i.name
                row['date'] = i.date
                row['task'] = i.task
                listObj.append(row)
            return listObj
        return json.JSONEncoder.default(self, obj)


class JSONSerializer:

    def serialize(self, obj, file):
        """
        Encode obj to json format and write it into file.
        """

        json.dump(obj, file, cls=NoteEncoder, sort_keys=True)

    def deserialize(self, file):
        """
....    Decode from json file to Python-object.
....    """

        return json.load(file)
