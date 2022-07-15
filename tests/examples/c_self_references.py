from dataclasses import dataclass
from typing import Optional, List

import marshy

from schemey.schema_context import schema_for_type

_Node = f"{__name__}.Node"


@dataclass
class Node:
    id: str
    children: Optional[List[_Node]] = None


schema = schema_for_type(Node)
schema_json = marshy.dump(schema.json_schema)
assert schema_json == {
    "$ref": "#$defs/Node",
    "$defs": {
        "Node": {
            "type": "object",
            "name": "Node",
            "additionalProperties": False,
            "properties": {
                "id": {"type": "string"},
                "children": {
                    "type": "array",
                    "items": {"$ref": "#$defs/Node"},
                    "default": None,
                },
            },
            "required": ["id"],
        }
    },
}
