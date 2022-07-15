from unittest import TestCase

from marshy import dump, load

from schemey.integer_schema import IntegerSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError
from schemey.schema_context import get_default_schema_context


class TestIntegerSchema(TestCase):
    def test_factory(self):
        context = get_default_schema_context()
        schema = context.get_schema(int)
        expected = IntegerSchema()
        self.assertEqual(expected, schema)

    def test_get_schema_errors(self):
        context = get_default_schema_context()
        schema = context.get_schema(int)
        self.assertEqual(list(schema.get_schema_errors(10)), [])
        self.assertEqual(
            list(schema.get_schema_errors(10.2)), [SchemaError("", "type", 10.2)]
        )
        self.assertEqual(
            list(schema.get_schema_errors(10.2, [])), [SchemaError("", "type", 10.2)]
        )
        self.assertEqual(
            list(schema.get_schema_errors(10.2, ["foo", "bar"])),
            [SchemaError("foo/bar", "type", 10.2)],
        )

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.get_schema(int)
        # noinspection PyTypeChecker
        schema.validate(10)
        with self.assertRaises(SchemaError):
            # noinspection PyTypeChecker
            schema.validate("foobar")

    def test_validate_fail(self):
        context = get_default_schema_context()
        schema = context.get_schema(int)
        with self.assertRaises(SchemaError):
            # noinspection PyTypeChecker
            schema.validate(10.5)

    def test_schema_minimum(self):
        schema = IntegerSchema(minimum=10)
        self.assertEqual(list(schema.get_schema_errors(11)), [])
        self.assertEqual(list(schema.get_schema_errors(10)), [])
        self.assertEqual(
            list(schema.get_schema_errors(9, ["foobar"])),
            [SchemaError("foobar", "minimum", 9)],
        )

    def test_schema_minimum_exclusive(self):
        schema = IntegerSchema(exclusive_minimum=10)
        self.assertEqual(list(schema.get_schema_errors(11)), [])
        self.assertEqual(
            list(schema.get_schema_errors(10)),
            [SchemaError("", "exclusive_minimum", 10)],
        )
        self.assertEqual(
            list(schema.get_schema_errors(9, ["foobar"])),
            [SchemaError("foobar", "exclusive_minimum", 9)],
        )

    def test_schema_maximum(self):
        schema = IntegerSchema(maximum=10)
        self.assertEqual(list(schema.get_schema_errors(9)), [])
        self.assertEqual(list(schema.get_schema_errors(10)), [])
        self.assertEqual(
            list(schema.get_schema_errors(11, ["foobar"])),
            [SchemaError("foobar", "maximum", 11)],
        )

    def test_schema_maximum_exclusive(self):
        schema = IntegerSchema(exclusive_maximum=10)
        self.assertEqual(list(schema.get_schema_errors(9)), [])
        self.assertEqual(
            list(schema.get_schema_errors(10)),
            [SchemaError("", "exclusive_maximum", 10)],
        )
        self.assertEqual(
            list(schema.get_schema_errors(11, ["foo"])),
            [SchemaError("foo", "exclusive_maximum", 11)],
        )

    def test_dump_and_load(self):
        schema = IntegerSchema()
        dumped = dump(schema)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_with_range(self):
        schema = IntegerSchema(minimum=5, maximum=9)
        dumped = dump(schema)
        expected_dump = dict(type="integer", minimum=5, maximum=9)
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_with_exclusive_range(self):
        schema = IntegerSchema(exclusive_minimum=4, exclusive_maximum=10)
        dumped = dump(schema)
        expected_dump = dict(type="integer", exclusiveMinimum=4, exclusiveMaximum=10)
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_simplify(self):
        self.assertEqual(
            dict(type="integer", exclusiveMinimum=5),
            dump(IntegerSchema(minimum=5, exclusive_minimum=5).simplify()),
        )
        self.assertEqual(
            dict(type="integer", exclusiveMinimum=5),
            dump(IntegerSchema(minimum=4, exclusive_minimum=5).simplify()),
        )
        self.assertEqual(
            dict(type="integer", minimum=6),
            dump(IntegerSchema(minimum=6, exclusive_minimum=5).simplify()),
        )
        self.assertEqual(
            dict(type="integer", exclusiveMaximum=5),
            dump(IntegerSchema(maximum=5, exclusive_maximum=5).simplify()),
        )
        self.assertEqual(
            dict(type="integer", exclusiveMaximum=5),
            dump(IntegerSchema(maximum=6, exclusive_maximum=5).simplify()),
        )
        self.assertEqual(
            dict(type="integer", maximum=4),
            dump(IntegerSchema(maximum=4, exclusive_maximum=5).simplify()),
        )
