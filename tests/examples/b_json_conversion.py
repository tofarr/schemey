import json

import marshy

from tests.examples.a_hello_world import (
    schema,
)  # Continuing from the previous example...

schema_json = marshy.dump(schema.json_schema)  # Convert to json_schema using marshy
json_str = json.dumps(schema_json)  # Dump to a string using the standard library

assert schema_json == {
    "type": "object",
    "name": "HelloWorld",
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "default": None},
        "friend": {"type": "boolean", "default": None},
    },
    "required": ["name"],
}
