import psycopg2
import pymysql
import sqlite3
import configparser

from querybuilder import QueryBuilder
from serializers import Serialize


class DataBase (object):
    """ Main database class """

    _books = []
    _authors = []
    _lib = []

    _instance = None
    _serialize = Serialize()

    @staticmethod
    def getInstance():
        """
        Returns database instance which is created only once
        >>> res1 = DataBase.getInstance()
        >>> res1 == DataBase.getInstance()
        True
        """
        if DataBase._instance is None:
            DataBase._instance = DataBase()
        return DataBase._instance

    def add(self, data, storage):
        """
        Adds `data` into `storage` in database
        >>> DataBase.getInstance().clear()
        >>> DataBase.getInstance()._books
        []
        >>> DataBase.getInstance().add(1, 'books')
        2
        >>> DataBase.getInstance()._books
        [1]
        """
        getattr(self, "_" + storage).append(data)
        return self.lastId(storage)

    def get(self, storage):
        """
        Returns `storage` form database
        >>> DataBase.getInstance().clear()
        >>> DataBase.getInstance().get('authors')
        []
        >>> DataBase.getInstance().add(1, 'authors')
        2
        >>> DataBase.getInstance().get('authors')
        [1]
        """
        return getattr(self, "_" + storage)

    def lastId(self, storage):
        """
        Returns last id in the `storage` plus 1
        >>> DataBase().getInstance().clear()
        >>> DataBase.getInstance().lastId('lib')
        1
        >>> DataBase.getInstance().add(1, 'lib')
        2
        >>> DataBase.getInstance().lastId('lib')
        2
        """
        return len(getattr(self, "_" + storage)) + 1

    def find(self, storage, key, value):
        """
        Returns a list of elements from `storage` for which field
        `key` is equal to value
        >>> db = DataBase().getInstance()
        >>> db.clear()
        >>> db.get('books')
        []
        >>> db.find('books', 'a', 'a')
        []
        >>> db.add(type('a', (), {'id': 1, 'a': 1})(), 'books')
        2
        >>> db.add(type('a', (), {'id': 2, 'a': 2})(), 'books')
        3
        >>> db.add(type('a', (), {'id': 3, 'a': 1})(), 'books')
        4
        >>> [x.id for x in db.find('books', 'a', 1)]
        [1, 3]
        """
        return [x for x in self.get(storage) if getattr(x, key) == value]

    def saveDataBase(self):
        """
        Saves database on disk
        >>> db = DataBase.getInstance()
        >>> db.clear()
        >>> db.loadDataBase()
        >>> db.saveDataBase()
        """
        self._serialize.save("books", self._books)
        self._serialize.save("authors", self._authors)
        self._serialize.save("lib", self._lib)

    def clear(self):
        """
        Clears database
        >>> db = DataBase.getInstance()
        >>> db._books = [1]
        >>> db._authors = [2]
        >>> db._lib = [3]
        >>> db.clear()
        >>> db._books
        []
        >>> db._authors
        []
        >>> db._lib
        []
        """
        self._lib = []
        self._authors = []
        self._books = []

    def loadDataBase(self):
        """
        Loads database from disk
        >>> db = DataBase.getInstance()
        >>> db.clear()
        >>> db._lib
        []
        >>> db._authors
        []
        >>> db._books
        []
        >>> db.loadDataBase()
        >>> db._lib == []
        False
        >>> db._authors == []
        False
        >>> db._books == []
        False
        """
        self._lib = self._serialize.load("lib")
        self._authors = self._serialize.load("authors")
        self._books = self._serialize.load("books")


class RelateDataBase:

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read('config.cfg')
        if 'DataBase' in conf:
            db = conf['DataBase']['db']
            if db == 'MysqlDataBase':
                self.db = MysqlDataBase()
            elif db == 'SqliteDataBase':
                self.db = SqliteDataBase()
            elif db == 'PostgresDataBase':
                self.db = PostgresDataBase()


    def add(self, data, storage):
        return self.db.insert(storage, data)

    def get(self, storage):
        return self.db.select(storage)

    def lastId(self, storage):
        pass

    def find(self, storage, key, value):
        return self.db.select(
            storage,
            fields=None,
            where=[{key: value}, []])

    def remove(self, key, value, storage):
        return self.db.delete(storage, [{key: value}, []])

    def clear(self):
        pass

    def saveDataBase(self):
        self.db.close_connection()

    def loadDataBase(self):
        pass


class PostgresDataBase:
    connector = None

    def __init__(self):
        self.connector = psycopg2.connect(
            dbname='phonebook',
            user='postgres',
            password='1111',
            cursor_factory=psycopg2.extras.RealDictCursor)

    def insert(self, table, data):
        with self.connector.cursor() as cursor:
            cursor.execute(
                QueryBuilder('%s').insert(table, list(data.keys())) + ' returning id',
                (list(data.values())))
            res = cursor.fetchone()['id']
        self.connector.commit()
        return res

    def select(self, table, fields=None, where=None):
        with self.connector.cursor() as cursor:
            cursor.execute(QueryBuilder('%s').select(table, fields, where))
            res = cursor.fetchall()
        return res if res != [] else None

    def update(self, table, data, where):
        with self.connector.cursor() as cursor:
            cursor.execute(
                QueryBuilder('%s').update(table, list(data.keys()), where),
                list(data.values()))
            res = cursor.rowcount
        self.connector.commit()
        return res

    def delete(self, table, where):
        with self.connector.cursor() as cursor:
            cursor.execute(QueryBuilder('%s').delete(table, where))
            res = cursor.rowcount
        self.connector.commit()
        return res

    def close_connection(self):
        self.connector.close()


class SqliteDataBase:
    connector = None

    def __init__(self):
        self.connector = sqlite3.connect('./database/dump/library.db')
        self.connector.row_factory = SqliteDataBase._dict_factory

    def insert(self, table, data):
        cursor = self.connector.cursor()
        cursor.execute(
            QueryBuilder('?').insert(table, list(data.keys())),
            (list(data.values())))
        self.connector.commit()
        return cursor.lastrowid

    def select(self, table, fields=None, where=None):
        cursor = self.connector.cursor()
        cursor.execute(
            QueryBuilder('?').select(table, fields, where))
        res = cursor.fetchall()
        return res if res != [] else None

    def update(self, table, data, where):
        cursor = self.connector.cursor()
        cursor.execute(
            QueryBuilder('?').update(table, list(data.keys()), where),
            list(data.values()))
        self.connector.commit()
        return cursor.rowcount

    def delete(self, table, where):
        cursor = self.connector.cursor()
        cursor.execute(
            QueryBuilder('?').delete(table, where))
        self.connector.commit()
        return cursor.rowcount

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def close_connection(self):
        self.connector.close()


class MysqlDataBase:
    connector = None

    def __init__(self):
        self.connector = pymysql.connect(
            host='localhost',
            user='root',
            passwd='12345678',
            db='library',
            cursorclass=pymysql.cursors.DictCursor)

    def insert(self, table, data):
        self.connector.begin()
        with self.connector.cursor() as cursor:
            cursor.execute(
                QueryBuilder('%s').insert(table, list(data.keys())),
                (list(data.values())))
        self.connector.commit()
        return cursor.lastrowid

    def select(self, table, fields=None, where=None):
        with self.connector.cursor() as cursor:
            cursor.execute(QueryBuilder('%s').select(table, fields, where))
            res = cursor.fetchall()
        return res if res != () else None

    def update(self, table, data, where):
        self.connector.begin()
        with self.connector.cursor() as cursor:
            cursor.execute(
                QueryBuilder('%s').update(table, list(data.keys()), where),
                list(data.values()))
        self.connector.commit()
        return cursor.rowcount

    def delete(self, table, where):
        self.connector.begin()
        with self.connector.cursor() as cursor:
            cursor.execute(
                QueryBuilder('%s').delete(table, where))
        self.connector.commit()
        return cursor.rowcount

    def close_connection(self):
        self.connector.close()


class Table:
    """
    Class for representing table in database
    """
    _db = None

    @staticmethod
    def initDataBase():
        if Table._db is None:
            Table._db = RelateDataBase()

    def save(self, obj, storage):
        """
        Adds `obj` into `storage` in database of table `self`
        >>> DataBase.getInstance().clear()
        >>> t = Table()
        >>> DataBase.getInstance()._books
        []
        >>> t.save(1, 'books')
        2
        >>> DataBase.getInstance()._books
        [1]
        """
        Table.initDataBase()
        try:
            return self._db.add(obj, storage)
        except:
            return -1

    def remove(self, key, value, storage):
        return self._db.remove(key, value, storage)

    @staticmethod
    def getLastId(storage):
        """
        Returns last id in the `storage` plus 1
        >>> DataBase().getInstance().clear()
        >>> Table.getLastId('lib')
        1
        >>> DataBase.getInstance().add(1, 'lib')
        2
        >>> Table.getLastId('lib')
        2
        """
        Table.initDataBase()
        return Table._db.lastId(storage)

    @staticmethod
    def listAll(storage):
        """
        Returns `storage` form database
        >>> DataBase.getInstance().clear()
        >>> Table.listAll('authors')
        []
        >>> DataBase.getInstance().add(1, 'authors')
        2
        >>> Table.listAll('authors')
        [1]
        """
        Table.initDataBase()
        res = Table._db.get(storage)
        if res is None:
            return []
        return res

    @staticmethod
    def find(storage, key, value):
        """
        Returns a list of elements from `storage` for which field
        `key` is equal to value
        >>> db = DataBase().getInstance()
        >>> db.clear()
        >>> db.get('books')
        []
        >>> db.find('books', 'a', 'a')
        []
        >>> db.add(type('a', (), {'id': 1, 'a': 1})(), 'books')
        2
        >>> db.add(type('a', (), {'id': 2, 'a': 2})(), 'books')
        3
        >>> db.add(type('a', (), {'id': 3, 'a': 1})(), 'books')
        4
        >>> [x.id for x in db.find('books', 'a', 1)]
        [1, 3]
        """
        Table.initDataBase()
        return Table._db.find(storage, key, value)

    def isPossibleType(self, value, _type):
        """
        Checks if `value` is of type `_type`
        >>> x = Table()
        >>> x.isPossibleType(1, int)
        >>> x.isPossibleType('asd', int)
        Traceback (most recent call last):
        ...
        TypeError: str is not of type int
        """
        Table.initDataBase()
        objClassName = value.__class__.__name__
        clName = _type.__name__
        if type(value) != _type:
            raise TypeError(objClassName + " is not of type " + clName)

    def __cmp__(self, otherObject):
        """
        Compares this Table instance to `otherObject`
        >>> x = Table()
        >>> y = Table()
        >>> x.__cmp__(y)
        True
        >>> x.a = 1
        >>> x.__cmp__(y)
        False
        >>> y.a = 1
        >>> x.__cmp__(y)
        True"""
        return self.__dict__ == otherObject.__dict__

    def initTable(self, d):
        self.__dict__ = d
