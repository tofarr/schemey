from dataclasses import dataclass
from enum import Enum
from unittest import TestCase

from marshy import load, dump

from schemey.enum_schema import EnumSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError
from schemey.schema_context import get_default_schema_context, schema_for_type


class MyEnum(Enum):
    FOO = 'foo'
    BAR = 'bar'
    ZAP = 'zap'
    BANG = 'bang'


class TestEnumSchema(TestCase):

    def test_factory(self):
        context = get_default_schema_context()
        schema = context.get_schema(MyEnum)
        expected = EnumSchema(name='MyEnum', enum={'foo', 'bar', 'zap', 'bang'})
        self.assertEqual(expected, schema)

    def test_get_schema_errors(self):
        schema = schema_for_type(MyEnum)
        self.assertEqual([], list(schema.get_schema_errors(MyEnum.FOO)))
        self.assertEqual([], list(schema.get_schema_errors(MyEnum.BAR)))
        self.assertEqual([], list(schema.get_schema_errors(MyEnum.BANG)))
        self.assertEqual([SchemaError('', 'type', 'pop')], list(schema.get_schema_errors('pop')))
        self.assertEqual([SchemaError('a/b', 'type', 'pop')], list(schema.get_schema_errors('pop', ['a', 'b'])))
        s = schema.json_schema
        self.assertEqual([SchemaError('a/b', 'value_not_permitted', 1)], list(s.get_schema_errors(1, ['a', 'b'])))

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.get_schema(MyEnum)
        with self.assertRaises(SchemaError):
            # noinspection PyTypeChecker
            schema.validate(10)

    def test_dump_and_load(self):
        schema = EnumSchema(name='foobar', enum={'foo', 'bar', 'zap', 'bang'}, description='Foobar')
        dumped = dump(schema)
        expected_dump = dict(name='foobar', enum=list(schema.enum), description='Foobar')
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_get_normalized_type(self):
        existing_types = {}
        schema = EnumSchema(name='Foobar', enum={'foo', 'bar', 'zap', 'bang'})
        standard_type = schema.get_normalized_type(existing_types, dataclass)
        self.assertTrue(issubclass(standard_type, Enum))
        # noinspection PyTypeChecker
        self.assertEqual({'foo', 'bar', 'zap', 'bang'}, set(s.name for s in standard_type))
        # noinspection PyTypeChecker
        self.assertEqual({'foo', 'bar', 'zap', 'bang'}, set(s.value for s in standard_type))
        self.assertIs(standard_type, schema.get_normalized_type(existing_types, dataclass))
