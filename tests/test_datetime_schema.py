from datetime import datetime
from unittest import TestCase

from marshy.default_context import new_default_context

from schemey.datetime_schema import DatetimeSchema
from schemey.schema_abc import SchemaABC
from schemey.number_schema import NumberSchema
from schemey.schema_error import SchemaError

N4 = datetime.fromisoformat('2021-11-04')
N5 = datetime.fromisoformat('2021-11-05')
N6 = datetime.fromisoformat('2021-11-06')


class TestNumberSchema(TestCase):

    def test_schema(self):
        schema = DatetimeSchema()
        assert list(schema.get_schema_errors(datetime.now(), {})) == []
        assert list(schema.get_schema_errors('foo', {})) == [SchemaError('', 'type', 'foo')]

    def test_schema_minimum(self):
        schema = DatetimeSchema(minimum=N5)
        assert list(schema.get_schema_errors(N6, {})) == []
        assert list(schema.get_schema_errors(N5, {})) == []
        schema_errors = list(schema.get_schema_errors(N4, {}, ['foobar']))
        assert schema_errors == [SchemaError('foobar', 'minimum', N4)]

    def test_schema_minimum_exclusive(self):
        schema = DatetimeSchema(minimum=N5, exclusive_minimum=True)
        assert list(schema.get_schema_errors(N6, {})) == []
        assert list(schema.get_schema_errors(N5, {})) == [SchemaError('', 'exclusive_minimum', N5)]
        assert list(schema.get_schema_errors(N4, {}, ['foobar'])) == [SchemaError('foobar', 'minimum', N4)]

    def test_schema_maximum(self):
        schema = DatetimeSchema(maximum=N5)
        assert list(schema.get_schema_errors(N4, {})) == []
        assert list(schema.get_schema_errors(N5, {})) == [SchemaError('', 'exclusive_maximum', N5)]
        assert list(schema.get_schema_errors(N6, {}, ['foobar'])) == [SchemaError('foobar', 'maximum', N6)]

    def test_schema_maximum_exclusive(self):
        schema = DatetimeSchema(maximum=N5, exclusive_maximum=False)
        assert list(schema.get_schema_errors(N4, {})) == []
        assert list(schema.get_schema_errors(N5, {})) == []
        assert list(schema.get_schema_errors(N6, {}, ['foobar'])) == [SchemaError('foobar', 'maximum', N6)]

    def test_marshalling(self):
        context = new_default_context()
        assert context.load(DatetimeSchema, dict(type='string', format='date-time')) == DatetimeSchema()
        json_schema = dict(type='string', format='date-time', minimum=N4.isoformat(), maximum=N6.isoformat(),
                           exclusiveMinimum=True, exclusiveMaximum=False)
        schema = DatetimeSchema(minimum=N4, maximum=N6, exclusive_minimum=True, exclusive_maximum=False)
        assert context.load(SchemaABC, json_schema) == schema
        assert context.dump(schema) == json_schema
