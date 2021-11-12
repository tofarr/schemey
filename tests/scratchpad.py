from dataclasses import dataclass
from typing import List, Iterator, Optional, Type
import json
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.json_output_context import JsonOutputContext
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError
from schemey.object_schema import ObjectSchema
from schemey.property_schema import PropertySchema
from schemey.array_schema import ArraySchema
from schemey.number_schema import NumberSchema
from schemey.schema_context import schema_for_type


@dataclass
class Point:
    x: float
    y: float

    @classmethod
    def __marshaller_factory__(cls, marshaller_context):
        """ Custom marshaller """
        return PointMarshaller()

    @classmethod
    def __schema_factory__(cls, schema_context):
        return PointSchema()


class PointMarshaller(MarshallerABC):
    def __init__(self):
        super().__init__(Point)

    def load(self, item):
        return Point(item[0], item[1])

    def dump(self, item):
        return [item.x, item.y]

    @classmethod
    def __marshaller_factory__(cls, marshaller_context):
        """ Custom marshaller """
        return PointMarshaller()


INTERNAL_SCHEMA = ObjectSchema(Point, (
    PropertySchema('x', NumberSchema(), required=True),
    PropertySchema('y', NumberSchema(), required=True)
))

EXTERNAL_SCHEMA = ArraySchema(NumberSchema(), 2, 2)


@dataclass
class PointSchema(SchemaABC[Point]):

    def get_schema_errors(self,
                          item: Point,
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        yield from INTERNAL_SCHEMA.get_schema_errors(item, current_path)

    @property
    def item_type(self) -> Type[Point]:
        return Point

    @property
    def default_value(self) -> Optional[Point]:
        return None

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> ExternalItemType:
        json_schema = EXTERNAL_SCHEMA.to_json_schema(json_output_context)
        return json_schema


schema = schema_for_type(Point)
schema.validate(Point(1.2, 3.4))
json_schema = schema.to_json_schema()
json_str = json.dumps(json_schema)

