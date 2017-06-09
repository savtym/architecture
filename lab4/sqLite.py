import sqlite3
from querybuilder import QueryBuilder


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

