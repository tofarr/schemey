from unittest import TestCase

from marshy import load, dump

from schema.any_of_schema import AnyOfSchema
from schema.enum_schema import EnumSchema
from schema.null_schema import NullSchema
from schema.ref_schema import RefSchema
from schema.schema_abc import SchemaABC
from schema.number_schema import NumberSchema
from schema.object_schema import ObjectSchema
from schema.property_schema import PropertySchema
from schema.schema_context import schema_for_type
from schema.schema_error import SchemaError
from schema.string_schema import StringSchema
from schema.with_defs_schema import WithDefsSchema
from tests.fixtures import Transaction, TransactionStatus


class TestObjectSchema(TestCase):

    def test_factory(self):
        schema = schema_for_type(Transaction)
        expected = WithDefsSchema(
            defs={'Transaction': ObjectSchema(property_schemas=(
                PropertySchema(name='id', schema=AnyOfSchema(schemas=(
                    StringSchema(),
                    NumberSchema(int),
                    NullSchema()))),
                PropertySchema(name='transaction_status', schema=AnyOfSchema(schemas=(
                    NullSchema(),
                    EnumSchema(permitted_values=('pending', 'rejected', 'completed')))))))
            },
            schema=RefSchema(ref='Transaction')
        )
        assert expected == schema

    def test_marshalling(self):
        schema = schema_for_type(Transaction)
        dumped = dump(schema)
        loaded = load(SchemaABC, dumped)
        assert loaded == schema

    def test_valid(self):
        schema = schema_for_type(Transaction)
        assert list(schema.get_schema_errors(Transaction(None, TransactionStatus.PENDING), {})) == []
        assert list(schema.get_schema_errors(Transaction(None, 'pending'), {}, ['foo'])) == []

    def test_invalid(self):
        schema = schema_for_type(Transaction)
        errors = list(schema.get_schema_errors(Transaction(None, 'PENDING'), {}, ['foo']))
        assert errors == [SchemaError('foo/transaction_status', 'value_not_permitted', 'PENDING')]
