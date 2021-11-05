from dataclasses import dataclass
from typing import List, Optional, Iterator, Dict
from unittest import TestCase

from marshy import ExternalType
from marshy.default_context import new_default_context

from schema.any_of_schema import optional_schema
from schema.array_schema import ArraySchema
from schema.boolean_schema import BooleanSchema
from schema.ref_schema import RefSchema
from schema.schema_abc import SchemaABC
from schema.number_schema import NumberSchema
from schema.object_schema import ObjectSchema
from schema.property_schema import PropertySchema
from schema.schema_context import schema_for_type, SchemaContext
from schema.schema_error import SchemaError
from schema.string_schema import StringSchema
from schema.with_defs_schema import WithDefsSchema
from tests.fixtures import Band, Issue


@dataclass
class DefinesSchema:
    @classmethod
    def __schema_factory__(cls, schema_context: SchemaContext, refs: Dict[str, SchemaABC]):
        return ObjectSchema((
            PropertySchema('some_bool', BooleanSchema()),
        ))


class TestSchema(TestCase):

    def test_schema_for_type_band(self):
        schema = schema_for_type(Band)
        expected = WithDefsSchema(
            defs={
                'Band': ObjectSchema(property_schemas=(
                    PropertySchema(name='id', schema=optional_schema(StringSchema())),
                    PropertySchema(name='band_name', schema=optional_schema(StringSchema())),
                    PropertySchema(name='year_formed', schema=optional_schema(NumberSchema(int)))
                ))
            },
            schema=RefSchema(ref='Band')
        )

        assert expected == schema
        assert not list(schema.get_schema_errors(Band(), {}))
        # noinspection PyTypeChecker
        assert len(list(schema.get_schema_errors(Band(23), {}))) == 1
        # noinspection PyTypeChecker
        assert len(list(schema.get_schema_errors(Band(23, False), {}))) == 2

    def test_schema_for_type_node(self):
        schema = schema_for_type(Issue)
        expected = WithDefsSchema(
            defs={
                'Issue': ObjectSchema(property_schemas=(
                    PropertySchema(name='id', schema=StringSchema()),
                    PropertySchema(name='tags', schema=ArraySchema(item_schema=StringSchema())),
                    PropertySchema(name='status', schema=RefSchema(ref='Status'))
                )),
                'Status': ObjectSchema(property_schemas=(
                    PropertySchema(name='title', schema=StringSchema()),
                    PropertySchema(name='public', schema=BooleanSchema())))
            },
            schema=RefSchema(ref='Issue')
        )
        assert expected == schema

    def test_schema(self):
        schema = schema_for_type(DefinesSchema)
        assert schema == DefinesSchema.__schema_factory__(SchemaContext(), {})

    def test_schema_invalid(self):

        class CantExtractSchema:
            pass

        with self.assertRaises(ValueError):
            schema_for_type(CantExtractSchema)

    def test_load_invalid(self):
        context = new_default_context()
        with self.assertRaises(KeyError):
            context.load(SchemaABC, dict(type='unknown'))

    def test_store_invalid(self):
        class WeirdSchema(SchemaABC):

            def get_schema_errors(self,
                                  item: ExternalType, refs: Dict[str, SchemaABC],
                                  current_path: Optional[List[str]] = None
                                  ) -> Iterator[SchemaError]:
                """ Never actually called"""

        context = new_default_context()
        with self.assertRaises(KeyError):
            context.dump(WeirdSchema())
        with self.assertRaises(KeyError):
            context.dump(dict(type='weird'), SchemaABC)
