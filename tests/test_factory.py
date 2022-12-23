"""
Use case below is a completely custom marshaller and schema for a type.
Coordinate3D objects will be marshalled as [x,y,z] (rather than {x:...,y:...,z:...})

Demonstrates flexibility of the system
"""

from dataclasses import dataclass
from typing import List, Dict, Type
from unittest import TestCase

import marshy
from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC

from schemey import Schema, schema_from_type


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
    def __schema_factory__(cls, context, path, ref_schemas: Dict[Type, Schema]):
        return Schema(
            dict(type="array", minLength=3, maxLength=3, items=dict(type="number")),
            Coordinate3D,
        )


class Coordinate3DMarshaller(MarshallerABC[Coordinate3D]):
    def load(self, item: ExternalType) -> Coordinate3D:
        return Coordinate3D(item[0], item[1], item[2])

    def dump(self, item: Coordinate3D) -> ExternalType:
        return [item.x, item.y, item.z]


class TestFactory(TestCase):
    def test_marshall_coordinate(self):
        coord = Coordinate3D(1, 2, 3)
        dumped = marshy.dump(coord)
        expected_dump = [1, 2, 3]
        self.assertEqual(expected_dump, dumped)
        loaded = marshy.load(Coordinate3D, dumped)
        self.assertEqual(coord, loaded)

    def test_load_and_dump_schema_for_coordinate(self):
        schema = schema_from_type(Coordinate3D)
        expected = Schema(
            {
                "type": "array",
                "minLength": 3,
                "maxLength": 3,
                "items": {"type": "number"},
            },
            Coordinate3D,
        )
        self.assertEqual(schema, expected)
        dumped = marshy.dump(schema)
        loaded = marshy.load(Schema, dumped)
        # Because we have given no other info on the python type, the type is assumed to be a list of floats!
        # Be careful generating types from schemas!
        expected_load = Schema(
            {
                "type": "array",
                "minLength": 3,
                "maxLength": 3,
                "items": {"type": "number"},
            },
            List[float],
        )
        self.assertEqual(expected_load, loaded)

    def test_schema_validate_for_coordinate(self):
        schema = schema_from_type(Coordinate3D)
        schema.validate([1, 3, 3])
