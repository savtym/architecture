class QueryBuilder:
    """
    Build query with given parameters
    """
    symbol = ''

    def __init__(self, symbol):
        self.symbol = symbol

    def insert(self, table, keys):
        """
        build insert query for table with fields(keys)
        """
        return 'insert into %s (%s) values (%s)' % \
               (table, ', '.join(keys), ', '.join([self.symbol] * len(keys)))

    def select(self, table, fields=None, where=None):
        """
        build select query for table or some tables with fields or
        for all fields (if fields == None) and with where part,
        for finding in database
        """
        where = self._get_where(where) if where is not None else ''
        table = ', '.join(table) if type(table) is list else table
        fields = '*' if fields is None else ', '.join(fields)
        return ('select %s from %s ' % (fields, table)) + where

    def update(self, table, keys, where):
        """
        build update query for table with fields(keys) with where
        """
        sql = 'update %s set %s = %s ' % \
              (table, ', '.join(keys), ', '.join([self.symbol] * len(keys)))
        return sql + self._get_where(where)

    def delete(self, table, where):
        """
        build delete query for table with where
        """
        return ('delete from %s ' % table) + self._get_where(where)

    def _get_where(self, where):
        """
        create where part of queries from given params
        """
        key_value = where[0]
        predicates = where[1]
        i = 0
        where_str = ''
        for k, v in zip(list(key_value.keys()), list(key_value.values())):
            where_str += k + ' = \'' + str(v) + '\''
            if i < len(where[1]):
                where_str += ' ' + predicates[i] + ' '
                i += 1
        return 'where ' + where_str
