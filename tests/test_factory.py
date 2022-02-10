"""
Use case below is a completely custom marshaller and schema for a type.
Coordinate3D objects will be marshalled as [x,y,z] (rather than {x:...,y:...,z:...})

Demonstrates flexibility of the system
"""

from dataclasses import dataclass
from typing import Optional, List, Iterator, Dict, Any, Type, Callable
from unittest import TestCase

import marshy
from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_abc import SchemaABC
from schemey.loader.schema_loader_abc import SchemaLoaderABC
from schemey.schema_error import SchemaError
from schemey.schema_context import schema_for_type, get_default_schema_context


@dataclass
class Coordinate3D:
    x: float
    y: float
    z: float

    # noinspection PyUnusedLocal
    @classmethod
    def __marshaller_factory__(cls, marshaller_context):
        return Coordinate3DMarshaller(Coordinate3D)

    # noinspection PyUnusedLocal
    @classmethod
    def __schema_factory__(cls, json_context):
        return Coordinate3DSchema()


class Coordinate3DMarshaller(MarshallerABC[Coordinate3D]):

    def load(self, item: ExternalType) -> Coordinate3D:
        return Coordinate3D(item[0], item[1], item[2])

    def dump(self, item: Coordinate3D) -> ExternalType:
        return [item.x, item.y, item.z]


@dataclass
class Coordinate3DSchema(SchemaABC):

    def get_schema_errors(self, item: ExternalItemType, current_path: Optional[List[str]] = None
                          ) -> Iterator[SchemaError]:
        if not isinstance(item, list) or len(item) != 3:
            yield SchemaError(current_path, 'invalid_point', item)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        return dict(
            type='array',
            minLength=3,
            maxLength=3,
            items=dict(type='number')
        )

    def get_normalized_type(self, existing_types: Dict[str, Any], object_wrapper: Callable) -> Type:
        # Standard type does not support tuples, because there are no tuples in graphql
        return List[float]


@dataclass
class Coordinate3DSchemaLoader(SchemaLoaderABC):
    priority: int = 200

    def load(self, item: ExternalItemType, json_context: JsonSchemaContext) -> Optional[SchemaABC]:
        if item.get('type') == 'array' and item.get('minLength') == 3 and item.get('maxLength') == 3:
            return Coordinate3DSchema()


get_default_schema_context().register_loader(Coordinate3DSchemaLoader())


class TestFactory(TestCase):

    def test_marshall_coordinate(self):
        coord = Coordinate3D(1, 2, 3)
        dumped = marshy.dump(coord)
        expected_dump = [1, 2, 3]
        self.assertEqual(expected_dump, dumped)
        loaded = marshy.load(Coordinate3D, dumped)
        self.assertEqual(coord, loaded)

    def test_schema_for_coordinate(self):
        schema = schema_for_type(Coordinate3D)
        self.assertEqual([1, 2, 3], marshy.dump(Coordinate3D(1, 2, 3)))
        self.assertEqual([SchemaError('', 'type', 'foo')], list(schema.get_schema_errors('foo')))
        self.assertEqual([], list(schema.get_schema_errors(Coordinate3D(1, 2, 3))))
        self.assertEqual([], list(schema.json_schema.get_schema_errors([1, 2, 3])))
        self.assertEqual([SchemaError('', 'invalid_point', 'foo')], list(schema.json_schema.get_schema_errors('foo')))

    def test_dump_and_load_schema(self):
        schema = schema_for_type(Coordinate3D).json_schema
        dumped = marshy.dump(schema)
        expected_dumped = {'items': {'type': 'number'}, 'maxLength': 3, 'minLength': 3, 'type': 'array'}
        self.assertEqual(dumped, expected_dumped)
        loaded = marshy.load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_get_normalized_type(self):
        schema = schema_for_type(Coordinate3D).json_schema
        standard_type = schema.get_normalized_type({}, dataclass)
        self.assertEqual(List[float], standard_type)
