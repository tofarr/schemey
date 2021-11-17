from unittest import TestCase
from uuid import uuid4, UUID

from schemey.schema_error import SchemaError
from schemey.uuid_schema import UuidSchema


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
        assert schema.to_json_schema() == dict(type='string', format='uuid')
        schema = UuidSchema(uuid4())
        assert schema.to_json_schema() == dict(type='string', format='uuid', default=str(schema.default_value))
