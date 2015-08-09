# -*- coding: utf-8 -*-

import datetime

import six
import sqlalchemy as sa
from dateutil.parser import parse as parse_date

from sandman import app
from sandman.model import utils
from sandman.exception import InvalidAPIUsage

converters = {
    datetime.datetime: parse_date,
    datetime.date: lambda value: parse_date(value).date,
}
def default_converter(column, value):
    column_type = utils._column_type(column)
    return column_type(value)

class Operator(object):

    def __call__(self, column, value):
        self.validate(column, value)
        return self.filter(column, self.convert(column, value))

    def convert(self, column, value):
        converter = converters.get(utils._column_type(column), default_converter)
        try:
            return converter(column, value)
        except Exception as error:
            raise InvalidAPIUsage(422)

    def validate(self, column, value):
        pass

    def filter(self, column, value):
        pass

class Equal(Operator):

    def filter(self, column, value):
        if app.config.get('CASE_INSENSITIVE') and issubclass(utils._column_type(column), six.string_types):
            return sa.func.upper(column) == value.upper()
        return column == value

class Like(Operator):

    def validate(self, column, value):
        if not issubclass(utils._column_type(column), six.string_types):
            raise InvalidAPIUsage(422)

    def filter(self, column, value):
        attr = 'ilike' if app.config.get('CASE_INSENSITIVE') else 'like'
        return getattr(column, attr)(value)

class GreaterThan(Operator):

    def filter(self, column, value):
        return column > value

class GreaterEqual(Operator):

    def filter(self, column, value):
        return column >= value

class LessThan(Operator):

    def filter(self, column, value):
        return column < value

class LessEqual(Operator):

    def filter(self, column, value):
        return column < value

operators = {
    'eq': Equal(),
    'gt': GreaterThan(),
    'gte': GreaterEqual(),
    'lt': LessThan(),
    'lte': LessEqual(),
    'like': Like(),
}

def parse_operator(key):
    parts = key.split('__')
    if len(parts) == 1:
        return parts[0], 'eq'
    elif len(parts) == 2:
        return parts
    raise InvalidAPIUsage(422, 'Invalid key "{0}"'.format(key))

def filter(model, key, value):
    column_name, operator_name = parse_operator(key)
    column = utils._get_column(model, column_name)
    try:
        operator = operators[operator_name]
    except KeyError:
        raise InvalidAPIUsage(422, 'Unknown operator "{0}"'.format(operator_name))
    return operator(column, value)
