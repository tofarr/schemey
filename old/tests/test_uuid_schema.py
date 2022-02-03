from dataclasses import dataclass
from unittest import TestCase
from uuid import uuid4, UUID

from schemey import GraphqlObjectType
from schemey import GraphqlContext
from schemey import SchemaABC
from schemey import schema_for_type
from schemey import SchemaError
from schemey import UuidSchema


class TestNumberSchema(TestCase):

    def test_schema(self):
        schema = UuidSchema()
        assert schema.item_type == UUID
        assert list(schema.get_schema_errors(uuid4())) == []
        # noinspection PyTypeChecker
        assert list(schema.get_schema_errors('foobar')) == [SchemaError('', 'type', 'foobar')]
        # noinspection PyTypeChecker
        assert list(schema.get_schema_errors('foobar', ['a', 'b'])) == [SchemaError('a/b', 'type', 'foobar')]

    def test_json_schema(self):
        schema = UuidSchema()
        assert schema.dump_json_schema() == dict(type='string', format='uuid')
        schema = UuidSchema(uuid4())
        assert schema.dump_json_schema() == dict(type='string', format='uuid', default=str(schema.default_value))

    def test_to_graphql(self):
        @dataclass
        class Entity:
            id: UUID

        schema: SchemaABC = schema_for_type(Entity)
        context = GraphqlContext(GraphqlObjectType.TYPE)
        schema.to_graphql_schema(context)
        graphql = context.to_graphql()
        expected = 'type Entity {\n\tid: ID!\n}\n\n'
        assert expected == graphql
