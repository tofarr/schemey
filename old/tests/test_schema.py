from dataclasses import dataclass
from unittest import TestCase

from schemey import __version__
from schemey import optional_schema
from schemey import BooleanSchema
from schemey import NumberSchema
from schemey import ObjectSchema
from schemey import PropertySchema
from schemey import SchemaContext, schema_for_type
from schemey import SchemaError
from schemey import StringSchema
from old.tests.fixtures import Band, Issue


# noinspection PyUnusedLocal
@dataclass
class DefinesSchema:
    @classmethod
    def __schema_factory__(cls, default_value, schema_context: SchemaContext):
        return ObjectSchema(DefinesSchema, (
            PropertySchema('some_bool', BooleanSchema()),
        ), default_value=default_value)


class TestSchema(TestCase):

    def test_schema_for_type_band(self):
        schema = schema_for_type(Band)
        expected = ObjectSchema(Band, property_schemas=(
            PropertySchema(name='id', schema=optional_schema(StringSchema())),
            PropertySchema(name='band_name', schema=optional_schema(StringSchema())),
            PropertySchema(name='year_formed', schema=optional_schema(NumberSchema(int)))
        ))

        assert expected == schema
        assert not list(schema.get_schema_errors(Band()))
        # noinspection PyTypeChecker
        assert len(list(schema.get_schema_errors(Band(23)))) == 1
        # noinspection PyTypeChecker
        assert len(list(schema.get_schema_errors(Band(23, False)))) == 2
        # noinspection PyTypeChecker
        with self.assertRaises(SchemaError):
            # noinspection PyTypeChecker
            schema.validate(Band(23, False))

    def test_schema_for_type_node(self):
        schema = schema_for_type(Issue)
        json_schema = schema.dump_json_schema()
        expected = {
            '$defs': {
                'Status': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string'},
                        'public': {'type': 'boolean'}
                    },
                    'additionalProperties': False
                },
                'Issue': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'tags': {'type': 'array', 'items': {'type': 'string'}},
                        'status': {'$ref': '#$defs/Status'}
                    },
                    'additionalProperties': False
                }
            },
            'allOf': [{'$ref': '#$defs/Issue'}]
        }
        assert expected == json_schema

    def test_schema(self):
        schema = schema_for_type(DefinesSchema)
        assert schema == DefinesSchema.__schema_factory__(None, SchemaContext())

    def test_schema_invalid(self):

        class CantExtractSchema:
            pass

        with self.assertRaises(ValueError):
            schema_for_type(CantExtractSchema)

    def test_version(self):
        assert __version__ is not None
