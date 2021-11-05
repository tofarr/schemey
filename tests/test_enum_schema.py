from unittest import TestCase

from marshy import load, dump

from schemey.any_of_schema import AnyOfSchema
from schemey.enum_schema import EnumSchema
from schemey.null_schema import NullSchema
from schemey.ref_schema import RefSchema
from schemey.schema_abc import SchemaABC
from schemey.number_schema import NumberSchema
from schemey.object_schema import ObjectSchema
from schemey.property_schema import PropertySchema
from schemey.schema_context import schema_for_type
from schemey.schema_error import SchemaError
from schemey.string_schema import StringSchema
from schemey.with_defs_schema import WithDefsSchema
from tests.fixtures import Transaction, TransactionStatus


class TestObjectSchema(TestCase):

    def test_factory(self):
        schema = schema_for_type(Transaction)
        expected = WithDefsSchema(
            defs={
                'Transaction': ObjectSchema(property_schemas=(
                    PropertySchema(name='id', schema=AnyOfSchema(schemas=(
                        StringSchema(),
                        NumberSchema(int),
                        NullSchema()))),
                    PropertySchema(name='transaction_status', schema=AnyOfSchema(schemas=(
                        NullSchema(),
                        EnumSchema(permitted_values=('pending', 'rejected', 'completed')))))
                ))
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
        # noinspection PyTypeChecker
        assert list(schema.get_schema_errors(Transaction(None, 'pending'), {}, ['foo'])) == []

    def test_invalid(self):
        schema = schema_for_type(Transaction)
        # noinspection PyTypeChecker
        errors = list(schema.get_schema_errors(Transaction(None, 'PENDING'), {}, ['foo']))
        assert errors == [SchemaError('foo/transaction_status', 'value_not_permitted', 'PENDING')]
