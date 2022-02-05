"""
Use case below is a completely custom marshaller and schema for a type.
Coordinate objects will be marshalled as [x,y] (rather than {x:...,y:...})

These changes are isolated to the CUSTOM_CONTEXT - the default is unaffected
Demonstrates flexibility of the system
"""
import copy
from dataclasses import dataclass
from typing import Optional, List, Iterator
from unittest import TestCase

import marshy
from marshy import ExternalType, new_default_context
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.factory.schema_marshaller_factory import SchemaMarshallerFactory
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_abc import SchemaABC
from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_error import SchemaError
from schemey.schemey_context import new_default_schemey_context, schema_for_type


@dataclass
class Coordinate:
    x: float
    y: float


class CoordinateMarshaller(MarshallerABC[Coordinate]):

    def load(self, item: ExternalType) -> Coordinate:
        return Coordinate(item[0], item[1])

    def dump(self, item: Coordinate) -> ExternalType:
        return [item.x, item.y]


@dataclass
class CoordinateSchema(SchemaABC):

    def get_schema_errors(self, item: ExternalItemType, current_path: Optional[List[str]] = None
                          ) -> Iterator[SchemaError]:
        if not isinstance(item, list) or len(item) != 2:
            yield SchemaError(current_path, 'invalid_point', item)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        return dict(
            type='array',
            minLength=2,
            maxLength=2,
            items=dict(type='number')
        )


@dataclass
class CoordinateSchemaLoader(SchemaLoaderABC):
    priority: int = 200

    def load(self, item: ExternalItemType, json_context: JsonSchemaContext) -> Optional[SchemaABC]:
        if item.get('type') == 'array' and item.get('minLength') == 2 and item.get('maxLength') == 2:
            return CoordinateSchema()


# The code below isolates the custom marshalling / schema from the defaults
CUSTOM_MARSHALLER_CONTEXT = new_default_context()
CUSTOM_MARSHALLER_CONTEXT.register_marshaller(CoordinateMarshaller(Coordinate))
CUSTOM_CONTEXT = new_default_schemey_context(CUSTOM_MARSHALLER_CONTEXT)
CUSTOM_CONTEXT.register_schema(Coordinate, CoordinateSchema())
CUSTOM_CONTEXT.register_loader(CoordinateSchemaLoader())
CUSTOM_MARSHALLER_CONTEXT.register_factory(SchemaMarshallerFactory(schemey_context=CUSTOM_CONTEXT, priority=201))


class TestCustomSchema(TestCase):

    def test_schema_for_coordinate(self):
        schema = CUSTOM_CONTEXT.get_obj_schema(Coordinate)
        self.assertEqual([1, 2], CUSTOM_CONTEXT.marshaller_context.dump(Coordinate(1, 2)))
        self.assertEqual([SchemaError('', 'type', 'foo')], list(schema.get_schema_errors('foo')))
        self.assertEqual([], list(schema.get_schema_errors(Coordinate(1, 2))))
        self.assertEqual([], list(schema.json_schema.get_schema_errors([1, 2])))

    def test_is_isolated_from_default(self):
        schema = schema_for_type(Coordinate)
        self.assertEqual(dict(x=1, y=2), marshy.dump(Coordinate(1, 2)))
        self.assertEqual([SchemaError('', 'type', 'foo')], list(schema.get_schema_errors('foo')))
        self.assertEqual([], list(schema.get_schema_errors(Coordinate(1, 2))))
        self.assertEqual([], list(schema.json_schema.get_schema_errors(dict(x=1, y=2))))

    def test_dump_and_load_schema(self):
        schema = CUSTOM_CONTEXT.get_schema(Coordinate)
        dumped = CUSTOM_MARSHALLER_CONTEXT.dump(schema)
        expected_dumped = {'items': {'type': 'number'}, 'maxLength': 2, 'minLength': 2, 'type': 'array'}
        self.assertEqual(dumped, expected_dumped)
        loaded = CUSTOM_MARSHALLER_CONTEXT.load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)
