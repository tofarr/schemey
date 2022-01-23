# Schemey - Json Schemas for Python.

This project allows for generation of json schema objects based on python
dataclasses, along with customization of said schemas. Schemas may then
be used to validate object graphs.

The framework is designed to be extensible, and out of the box support
is provided for dataclasses, enums, timestamps and primitives.

Serialization is provided using marshy.

## Why did you build this?

There were undocumented gaps in the functionality of existing solutions
that made using them untenable.

## Installation

`pip install schemey`

## Basic Usage

```
# Given a python dataclass:
from dataclasses import dataclass
from typing import Optional

@dataclass
class HelloWorld:
  name: str
  age: Optional[int] = None
  friend: Optional[bool] = None


# A schema may be generated...
from schemey.schema_context import schema_for_type
schema = schema_for_type(HelloWorld)

# A full listing of errors for an item can be retrieved:
errors = list(schema.get_schema_errors(HelloWorld(None)))  # [SchemaError(path='name', code='type', value='You')]

# ...or validation errors can be thrown:
schema.validate(HelloWorld('You'))  # No errors
# schema.validate(HelloWorld(None)) # raises SchemaError(path='name', code='type', value=None)

```

# Converting to / from Json Schemas:

Serialize schema instances to JSON schemas:
```
# Continuing from the previous example...
from schemey.schema_abc import SchemaABC
import json
json_schema = schema.to_json_schema()
json_str = json.dumps(json_schema)
```

The contents of `json_str` (formatted) will be:
```
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "age": {
      "anyOf": [
        { "type": "null" },
        { "type": "integer" }
      ]
    },
    "friend": {
      "anyOf": [
        { "type": "null" },
        { "type": "boolean" }
      ]
    }
  },
  "additionalProperties": false
}
```

Deserializing json schemas is currently not supported.
(Due to the complexity of extracting references from anywhere in
the document and the evolving nature of the spec). The intended 
workflow is to start with a Python dataclass and then convert to
a json schema rather than the other way around.

Self referencing data structures are supported out of the box. For
example...
```
@dataclass
class Node:
    id: str
    children: Optional[List[f'{__name__}.Node']] = None
```
...will result in the following schema:
```
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string"
    },
    "children": {
      "anyOf": [
        { "type": "null" },
        {
          "type": "array",
          "items": {
            "$ref": "#$defs/Node"
          }
        }
      ]
    }
  },
  "additionalProperties": false
}
```

## Adding constraints

### Specifying a schema for a field

```
from dataclasses import dataclass, field
from typing import Optional
from schemey.number_schema import NumberSchema
from schemey.schema_context import schema_for_type

@dataclass
class Person:
  name: str
  age: Optional[int] = field(default=None, metadata=dict(schema=NumberSchema(int, minimum=0)))

schema = schema_for_type(Person)

errors = list(schema.get_schema_errors(Person('You', -1)))  # [SchemaError(path='age', code='minimum', value=-1)]
```

The following schemas are defined out of the box (Feel free to add your own!):

* [AnyOfSchema](schemey/any_of_schema.py): For polymorphic constraints
* [ArraySchema](schemey/array_schema.py): For arrays
* [BooleanSchema](schemey/boolean_schema.py): For boolean values
* [DatetimeSchema](schemey/datetime_schema.py): For datetime values as iso strings
* [DeferredSchema](schemey/deferred_schema.py): Deferred schema - (used for self referential schemas)
* [EnumSchema](schemey/enum_schema.py): For enums
* [NumberSchema](schemey/number_schema.py): For integer / float validation
* [NullSchema](schemey/null_schema.py): For None / null values
* [ObjectSchema](schemey/object_schema.py): For objects
* [PropertySchema](schemey/property_schema.py): For properties of objects
* [RefSchema](schemey/deferred_schema.py): For indirectly referenced objects  
* [StringSchema](schemey/string_schema.py): For string validation. (Including regex, format and length constraints)

## Architectural Concepts.

* A [Schema](schemey/schema_abc.py) is used to validate instances of a type
* A [Factory](schemey/factory/schema_factory_abc.py) is used to create schemas for a given type
* A [Context](schemey/schema_context.py) coordinates the operations between schemas and factories (Using
  the default context leads to a shorter syntax, but less flexibility)

## Specifying a Schema for a Class

Below we outline the process of completely customizing schema generation and marshalling.
The simplest way to specify a schema for a class is to define the __schema_factory__ class
property. For example, imagine a situation where a 2D point is defined in javascript
as an array of 2 numbers, [x, y].

You write a dataclass to describe this in python, with a custom marshaller (As per the marshy
documentation), but the marshalled schema no longer matches the marshalled dataclass.
You will need to define a custom schema and marshaller for the class too:

```
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
    def __schema_factory__(cls, default_value, schema_context):
        return PointSchema()


class PointMarshaller(MarshallerABC):
    def __init__(self):
        super().__init__(Point)

    def load(self, item):
        return Point(item[0], item[1])

    def dump(self, item):
        return [item.x, item.y]


INTERNAL_SCHEMA = ObjectSchema(Point, (
    PropertySchema('x', NumberSchema(), required=True),
    PropertySchema('y', NumberSchema(), required=True)
))

EXTERNAL_SCHEMA = ArraySchema(NumberSchema(), 2, 2)


@dataclass
class PointSchema(SchemaABC[Point]):
    default_value: Optional[Point] = None

    def get_schema_errors(self,
                          item: Point,
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        yield from INTERNAL_SCHEMA.get_schema_errors(item, current_path)

    @property
    def item_type(self) -> Type[Point]:
        return Point

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> ExternalItemType:
        json_schema = EXTERNAL_SCHEMA.to_json_schema(json_output_context)
        return json_schema


schema = schema_for_type(Point)
schema.validate(Point(1.2, 3.4))
json_schema = schema.to_json_schema()
json_str = json.dumps(json_schema)
```

### Specify a Schema for a Class by factory

Instead of overriding the __schema_factory__ / __marshaller_factory__
methods, it is possible to register a factory for your schema with
your schema context using the `register_schema` method.

It is also possible to register implementations for abstract classes / duck typing via the 
[register_impl method](tests/factory/test_impl_schema_factory.py)


## Building The Project

You need an account on pypi before this will work:

```
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install twine
python -m twine upload dist/*
```