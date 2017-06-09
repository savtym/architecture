import psycopg2
from querybuilder import QueryBuilder


class PostgresDataBase:
    connector = None

    def __init__(self):
        self.connector = psycopg2.connect(
            dbname='phonebook',
            user='postgres',
            password='12345678',
            cursor_factory=psycopg2.extras.RealDictCursor)

    def insert(self, t, d):
        with self.connector.cursor() as cursor:
            cursor.execute(
                QueryBuilder('%s').insert(t, list(d.keys())) + ' returning id',
                (list(d.values())))
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
