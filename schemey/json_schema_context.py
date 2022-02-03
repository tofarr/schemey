from dataclasses import dataclass, field
from typing import List

from schemey.jsonifier.schema_jsonifier_abc import JsonSchemaMarshallerABC


@dataclass
class JsonSchemaContext:
    json_schema_marshallers: List[JsonSchemaMarshallerABC] = field(default_factory=list)


