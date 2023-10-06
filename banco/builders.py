from sqlalchemy import (create_engine, column, delete, select, distinct)
from sqlalchemy.orm.session import Session


class Operator(object):
    def __init__(self):
        ...

    def build(self):
        ...

class In_(object):

    def build(self, table, filter: dict, query):
        query = query.filter(getattr(table, filter['name']).in_(filter['value']))

        return query


class GenericOperation(object):

    def __init__(self):
        ...

    def build(self, table, filter: dict, query):

        column = getattr(table, filter['name'])
        operation = getattr(table, f'__{filter["op"]}__')
        filter_obj = getattr(column, operation.__name__)(filter['value'])

        query = query.filter(filter_obj)
        return query