import marshy
from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.marshaller_context import MarshallerContext

from schemey import SchemaContext, Schema
from schemey.validator import validator_from_type


# Custom marshalling / validations are supported...
# In the example below, we want a Point object to have the
# external format [x, y] - an array with 2 numbers


class Point:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # noinspection PyUnusedLocal
    @classmethod
    def __marshaller_factory__(cls, context: MarshallerContext):
        # Marshy already lets us define marshalling any way we choose.
        class PointMarshaller(MarshallerABC[Point]):

            def load(self, item: ExternalType) -> Point:
                return Point(*item)

            def dump(self, item: Point) -> ExternalType:
                return [item.x, item.y]

        return PointMarshaller(Point)

    # noinspection PyUnusedLocal
    @classmethod
    def __schema_factory__(cls, context: SchemaContext, path: str):
        # The simplest way to specify a schema for a class is to define the __schema_factory__ method
        # Here we define our schema in standard json...
        return Schema(
            {
                "type": "array",
                "minLength": 2,
                "maxLength": 2,
                "items": {
                    "type": "number",
                }
            },
            Point,
        )


validator = validator_from_type(Point)
point = marshy.load(Point, [4.0, 5.0])  # same as `point = Point(4.0, 5.0)`
validator.validate(point)
validator.schema.validate([4.0, 5.0])  # Go to the schema to check unmarshalled values
# validator.validate(Point(4.0, '5.0')) # raises ValidationError
