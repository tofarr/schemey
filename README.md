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
errors = list(schema.get_schema_errors(HelloWorld(None), {}))  # [SchemaError(path='name', code='type', value='You')]

# ...or validation errors can be thrown:
schema.validate(HelloWorld('You'))  # No errors
# schema.validate(HelloWorld(None)) # raises SchemaError(path='name', code='type', value=None)

```

# Converting to / from Json Schemas:

Serialize schema instances to JSON schemas using marshy:
```
# Continuing from the previous example...
from marshy import dump, load
from schemey.schema_abc import SchemaABC
import json
dumped = dump(schema)
json_str = json.dumps(dumped)
loaded = load(SchemaABC, dumped)
```

The contents of `json_str` (formatted) will be:
```
{
  "$defs": {
    "HelloWorld": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "age": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "type": "integer"
            }
          ]
        },
        "friend": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "type": "boolean"
            }
          ]
        }
      },
      "additionalProperties": false,
      "required": [
        "name"
      ]
    }
  },
  "allOf": [
    {
      "$ref": "#/$defs/HelloWorld"
    }
  ]
}
```

Deserializing json schemas is currently only partially supported.
(Due to the complexity of extracting references from anywhere in
the document). Schemas produced by schemey can be deserialized, 
but the intended workflow is to start with a Python dataclass
and then convert to a json schema rather than the other way around.

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

errors = list(schema.get_schema_errors(Person('You', -1), {}))  # [SchemaError(path='age', code='type', value=-1)]
```

The following schemas are defined out of the box (Feel free to add your own!):

* [AnyOfSchema](schemey/any_of_schema.py): For polymorphic constraints
* [ArraySchema](schemey/array_schema.py): For arrays
* [BooleanSchema](schemey/boolean_schema.py): For boolean values
* [DatetimeSchema](schemey/datetime_schema.py): For datetime values as iso strings
* [EnumSchema](schemey/enum_schema.py): For enums
* [NumberSchema](schemey/number_schema.py): For integer / float validation
* [NullSchema](schemey/null_schema.py): For None / null values
* [ObjectSchema](schemey/object_schema.py): For objects
* [PropertySchema](schemey/property_schema.py): For properties of objects
* [RefSchema](schemey/ref_schema.py): For indirectly referenced objects  
* [StringSchema](schemey/string_schema.py): For string validation. (Including regex, format and length constraints)
* [WithDefsSchema](schemey/with_defs_schema.py): For schemas which include indirectly referenced objects

### Specifying a Schema for a Class



### Specify a Schema for a Class by factory

Datetimes to numbers example