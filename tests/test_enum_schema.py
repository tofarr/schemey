from unittest import TestCase

from schemey.any_of_schema import AnyOfSchema
from schemey.enum_schema import EnumSchema
from schemey.null_schema import NullSchema
from schemey.number_schema import NumberSchema
from schemey.object_schema import ObjectSchema
from schemey.property_schema import PropertySchema
from schemey.schema_context import schema_for_type
from schemey.schema_error import SchemaError
from schemey.string_schema import StringSchema
from tests.fixtures import Transaction, TransactionStatus


class TestObjectSchema(TestCase):

    def test_factory(self):
        schema = schema_for_type(Transaction)
        expected = ObjectSchema(Transaction, property_schemas=(
            PropertySchema(name='id', required=True, schema=AnyOfSchema(schemas=(
                StringSchema(),
                NumberSchema(int),
                NullSchema()))),
            PropertySchema(name='transaction_status', schema=AnyOfSchema(schemas=(
                NullSchema(),
                EnumSchema(TransactionStatus))))
        ))
        assert expected == schema
        json_schema = {
            'type': 'object',
            'properties': {
                'id': {
                    'anyOf': [
                        {'type': 'string'},
                        {'type': 'integer'},
                        {'type': 'null'}]},
                'transaction_status': {
                    'anyOf': [
                        {'type': 'null'},
                        {'enum': ['pending', 'rejected', 'completed']}]}},
            'additionalProperties': False
        }
        dumped = schema.to_json_schema()
        assert dumped == json_schema

    def test_valid(self):
        schema = schema_for_type(Transaction)
        assert list(schema.get_schema_errors(Transaction(None, TransactionStatus.PENDING))) == []
        # noinspection PyTypeChecker
        assert list(schema.get_schema_errors(Transaction(None, 'pending'), ['foo'])) == []

    def test_invalid(self):
        schema = schema_for_type(Transaction)
        # noinspection PyTypeChecker
        errors = list(schema.get_schema_errors(Transaction(None, 'PENDING'), ['foo']))
        assert errors == [SchemaError('foo/transaction_status', 'value_not_permitted', 'PENDING')]

    def test_default_value(self):
        schema = EnumSchema(TransactionStatus, TransactionStatus.PENDING)
        json_schema = schema.to_json_schema()
        expected = dict(enum=[s.value for s in TransactionStatus], default='pending')
        assert expected == json_schema
