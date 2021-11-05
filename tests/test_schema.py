from dataclasses import dataclass, field
from typing import List, ForwardRef, Optional, Iterator
from unittest import TestCase

from marshy import ExternalType
from marshy.default_context import new_default_context

from persisty.schema.any_of_schema import optional_schema
from persisty.schema.array_schema import ArraySchema
from persisty.schema.boolean_schema import BooleanSchema
from persisty.schema.schema_abc import SchemaABC
from persisty.schema.number_schema import NumberSchema
from persisty.schema.object_schema import ObjectSchema
from persisty.schema.property_schema import PropertySchema
from persisty.schema.schema_context import schema_for_type, SchemaContext
from persisty.schema.schema_error import SchemaError
from persisty.schema.string_schema import StringSchema


@dataclass
class Node:
    id: str
    tags: List[str] = field(default_factory=list)
    status: ForwardRef(f'{__name__}.Status') = None


@dataclass
class Status:
    title: str
    public: bool = False


@dataclass
class DefinesSchema:
    @classmethod
    def __schema_factory__(cls, schema_context: SchemaContext):
        return ObjectSchema((
            PropertySchema('some_bool', BooleanSchema()),
        ))


@dataclass
class Band:
    id: Optional[str] = None
    band_name: Optional[str] = None
    year_formed: Optional[int] = None


class TestSchema(TestCase):

    def test_schema_for_type_band(self):
        schema = schema_for_type(Band)
        expected = ObjectSchema((
            PropertySchema('id', optional_schema(StringSchema())),
            PropertySchema('band_name', optional_schema(StringSchema())),
            PropertySchema('year_formed', optional_schema(NumberSchema(int))),
        ))
        assert expected == schema
        assert not list(schema.get_schema_errors({}))
        # noinspection PyTypeChecker
        assert len(list(schema.get_schema_errors(Band(23)))) == 1
        # noinspection PyTypeChecker
        assert len(list(schema.get_schema_errors(Band(23, False)))) == 2

    def test_schema_for_type_node(self):
        schema = schema_for_type(Node)
        expected = ObjectSchema((
            PropertySchema('id', StringSchema()),
            PropertySchema('tags', ArraySchema(StringSchema())),
            PropertySchema('status', ObjectSchema((
                PropertySchema('title', StringSchema()),
                PropertySchema('public', BooleanSchema())
            )))
        ))
        assert expected == schema

    def test_schema(self):
        schema = schema_for_type(DefinesSchema)
        assert schema == DefinesSchema.__schema_factory__(SchemaContext())

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

            def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None
                                  ) -> Iterator[SchemaError]:
                """ Never actually called"""

        context = new_default_context()
        with self.assertRaises(KeyError):
            context.dump(WeirdSchema())
        with self.assertRaises(KeyError):
            context.dump(dict(type='weird'), SchemaABC)
