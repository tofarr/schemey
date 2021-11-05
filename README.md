# Schemey - Object Schemas for Python.

This project allows for generation of json schema objects based on python
dataclasses, along with customization of said schemas. Schemas may then
be used to validate object graphs.

The framework is designed to be extensible, and out of the box support
is provided for dataclasses, enums, timestamps and primitives.

Serialization is provided using marshy.

## Installation

`pip install schemey`

## Basic Usage

Given a python dataclass:
```
from dataclasses import dataclass
from typing import Optional

@dataclass
class HelloWorld:
  name: str
  age: Optional[int] = None
  friend: Optional[bool] = None
```

A schema may be generated...
```
from schemey.schema_context import schema_for_type
schema = schema_for_type(HelloWorld)
```

...and then used to validate instances thus:
```
schema.validate(HelloWorld('You'))  # No errors
schema.validate(HelloWorld(None)) # raises SchemaError(path='name', code='type', value=None)
```

Alternatively, a full listing of errors for an item can be retrieved:
```
list(schema.get_schema_errors(HelloWorld(None), {}))  # [SchemaError(path='name', code='type', value='You')]
```

# Converting to / from Json Schemas:

Serialize schema instances to JSON schemas using marshy:
```
from marshy import dump, load
from schemey.schema_abc import SchemaABC
import json
dumped = dump(schema)
json_str = json.dumps(dumped)
loaded = load(SchemaABC, dumped)
```

The contents of `json_str` (formatted) will be:
```

```

Deserializing json schemas is currently only partially supported.
Schemas produced by schemey can be deserialized, but the intended
workflow is Python dataclass to json schema rather than the other 
way around.