import unittest
from io import StringIO, BytesIO

import jsonSerialization as jsSer
import yamlSerialization as yaSer
import pickleSerialization as piSer
import modelController as mc


class SerializationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mc = mc.ModelController()
        cls.mc.setNewEl('1', '01.01.2017', 'Desc of 1')
        cls.mc.setNewEl('2', '01.02.2017', 'Desc of 2')

    def test_pickleSave(self):
        first = BytesIO()
        piSer.PickleSerializer().serialize(self.mc, first)
        firstContent = first.getvalue()
        second = BytesIO()
        piSer.PickleSerializer().serialize(self.mc, second)
        secondContent = second.getvalue()
        self.assertEqual(firstContent, secondContent)

    def test_jsonSave(self):
        outfile = StringIO()
        jsSer.JSONSerializer().serialize(self.mc, outfile)
        outfile.seek(0)
        content = outfile.read()
        self.assertEqual(content,
                         '[{"date": "01.01.2017", "name": "1", ' +
                         '"task": "Desc of 1"},' +
                         ' {"date": "01.02.2017", "name": "2", ' +
                         '"task": "Desc of 2"}]')

    def test_yamlSave(self):
        outfile = StringIO()
        yaSer.YAMLSerializer().serialize(self.mc, outfile)
        outfile.seek(0)
        content = outfile.read()
        self.assertEqual(content,
                         "- !!python/object:notes.Note " +
                         "{date: 01.01.2017, name: '1', task: Desc of 1}\n" +
                         "- !!python/object:notes.Note " +
                         "{date: 01.02.2017, name: '2', task: Desc of 2}\n")

    def test_pickleLoad(self):
        outfile = BytesIO()
        piSer.PickleSerializer().serialize(self.mc, outfile)
        outfile.seek(0)
        content = piSer.PickleSerializer().deserialize(outfile)
        self.assertEqual(self.mc, content)

    def test_jsonLoad(self):
        outfile = StringIO()
        jsSer.JSONSerializer().serialize(self.mc, outfile)
        outfile.seek(0)
        content = jsSer.JSONSerializer().deserialize(outfile)
        self.assertCountEqual(str(content),
                              "[{'date': '01.01.2017', 'task': 'Desc of 1', " +
                              "'name': '1'}, " +
                              "{'date': '01.02.2017', 'task': 'Desc of 2', " +
                              "'name': '2'}]")

    def test_yaml_load(self):
        outfile = StringIO()
        yaSer.YAMLSerializer().serialize(self.mc, outfile)
        outfile.seek(0)
        content = yaSer.YAMLSerializer().deserialize(outfile)
        self.assertEqual(self.mc, content)


if __name__ == '__main__':
    unittest.main()
