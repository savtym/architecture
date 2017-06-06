import os
from unittest import TestCase

from generator import generator, generate
import yaml
import json

from serializestreamio import jsonSerializeToStream, yamlSerializeToStream
from models import Book, Library, Author
from serializers import PickleSerialize, YamlSerialize
from serializers import JsonSerialize, Serialize


@generator
class TestSerialize(TestCase):
    @generate(
        [[Book("b1"), Book("b2")], "tests/books"]
    )
    def test_save(self, data):
        serialize = Serialize()
        serialize.save(data[1], data[0])
        compareLists(data[0], serialize.load(data[1]), self.fail)


@generator
class TestPickleSerialize(TestCase):
    @generate(
        [[Book("b1"), Book("b2")], "tests/books"]
    )
    def test_save(self, data):
        PickleSerialize.save(data[1], data[0])
        compareLists(data[0], PickleSerialize.load(data[1]), self.fail)

    @generate(
        [[], "unreal-path/unreal-file"]
    )
    def test__getFromFile(self, data):
        compareLists(data[0], PickleSerialize.load(data[1]), self.fail)


@generator
class TestJsonSerialize(TestCase):
    @generate(
        [[Library(Book("book1"), Author("author1")),
            Library(Book("book1"), Author("author2"))], "tests/lib"]
    )
    def test_save(self, data):
        JsonSerialize.save(data[1], data[0])
        stream, ls = jsonSerializeToStream(data[0])
        self.assertListEqual(json.load(stream), ls)

    @generate(
        [[Library(Book("book1"), Author("author1")),
            Library(Book("book1"), Author("author2"))], "tests/lib"],
        [[], "unreal-path/unreal-file"]
    )
    def test__getFromFile(self, data):
        lst = []
        for i in JsonSerialize.load(data[1]):
            objDict = JsonSerialize._prepareSave(i.__dict__)
            lst.append([objDict, i.__class__.__name__])
        if not os.path.isfile("tables/json/" + data[1] + ".json"):
            return []
        with open("tables/json/" + data[1] + ".json") as f:
            self.assertListEqual(json.load(f), lst)


@generator
class TestYamlSerialize(TestCase):
    @generate(
        [[Book("b1"), Book("b2")], "tests/books"]
    )
    def test_save(self, data):
        YamlSerialize.save(data[1], data[0])
        stream = yamlSerializeToStream(data[0])
        compareLists(
            yaml.load(stream.read()),
            YamlSerialize.load(data[1]),
            self.fail)

    @generate(
        [[Book("b1"), Book("b2")], "tests/books"],
        [[], "unreal-path/unreal-file"],
        [[], "tables/tests/empty-file.yaml"]
    )
    def test__getFromFile(self, data):
        compareLists(data[0], YamlSerialize.load(data[1]), self.fail)


def compareLists(list1, list2, fail):
    for item1, item2 in zip(list1, list2):
        if not item1.__cmp__(item2):
            fail()


@generator
class TestCompareLists(TestCase):
    @generate(
        [[Book("b1"), Book("b2")], [Book("b1"), Book("b2")]],
        [[Book("b1"), Book("b2")], [Book("b4"), Book("b3")]]
    )
    def test_compareLists(self, data):
        try:
            compareLists(data[0], data[1], self.fail)
        except AssertionError:
            return
