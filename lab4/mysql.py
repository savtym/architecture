import pymysql
from querybuilder import QueryBuilder


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

