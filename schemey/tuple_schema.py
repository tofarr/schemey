from dataclasses import dataclass
from typing import Optional, List, Iterator, Tuple

from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.schema_abc import SchemaABC, _JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass
class TupleSchema(SchemaABC):
    items: Tuple[SchemaABC, ...]

    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if current_path is None:
            current_path = []
        if not isinstance(item, list) or len(item) != len(self.items):
            yield SchemaError(current_path, 'type', item)
            return
        for index, sub_item in enumerate(item):
            current_path.append(str(index))
            schema = self.items[index]
            yield from schema.get_schema_errors(sub_item, current_path)
            current_path.pop()

    def dump_json_schema(self, json_context: _JsonSchemaContext) -> ExternalItemType:
        schema = {
            "type": "array",
            "prefixItems": [i.dump_json_schema(json_context) for i in self.items],
            "items": False
        }
        return schema
