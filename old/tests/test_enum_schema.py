from unittest import TestCase

from schemey import AnyOfSchema
from schemey import EnumSchema
from schemey import GraphqlObjectType
from schemey import GraphqlContext
from schemey import NullSchema
from schemey import NumberSchema
from schemey import ObjectSchema
from schemey import PropertySchema
from schemey import schema_for_type
from schemey import SchemaError
from schemey import StringSchema
from old.tests.fixtures import Transaction, TransactionStatus


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
          '$defs': {
            'AnyOfStringIntNull': {
              'anyOf': [
                {'type': 'string'},
                {'type': 'integer'},
                {'type': 'null'}
              ]
            },
            'AnyOfNullTransactionStatus': {
              'anyOf': [
                {'type': 'null'},
                {'enum': ['pending', 'rejected', 'completed']}
              ]
            },
            'Transaction': {
              'type': 'object',
              'properties': {
                'id': {
                  '$ref': '#$defs/AnyOfStringIntNull'
                },
                'transaction_status': {
                  '$ref': '#$defs/AnyOfNullTransactionStatus'
                }
              },
              'additionalProperties': False
            }
          },
          'allOf': [
            {
              '$ref': '#$defs/Transaction'
            }
          ]
        }
        dumped = schema.dump_json_schema()
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
        json_schema = schema.dump_json_schema()
        expected = dict(enum=[s.value for s in TransactionStatus], default='pending')
        assert expected == json_schema

    def test_to_graphql(self):
        schema = EnumSchema(TransactionStatus, TransactionStatus.PENDING)
        graphql_context = GraphqlContext(GraphqlObjectType.INPUT)
        schema.to_graphql_schema(graphql_context)
        graphql = graphql_context.to_graphql()
        expected = '"""\nAn enumeration.\n"""\nenum TransactionStatus {\n\tpending\n\trejected\n\tcompleted\n}\n\n'
        assert graphql == expected
