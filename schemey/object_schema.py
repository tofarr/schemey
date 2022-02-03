from dataclasses import dataclass
from typing import Union, Optional, List, Iterator, Dict

from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class ObjectSchema(JsonSchemaABC):
    properties: Dict[str, JsonSchemaABC]
    name: Optional[str] = None
    default_value: Union[ExternalItemType, NoDefault] = NoDefault
    additional_properties: bool = False
    required: Optional[List[str]] = None

    def get_schema_errors(self, item: ExternalItemType, current_path: Optional[List[str]] = None
                          ) -> Iterator[SchemaError]:
        if not isinstance(item, dict):
            yield SchemaError(current_path, 'type', item)
            return
        keys = set(item.keys())
        for key, property_schema in self.properties.items():
            if key in keys:
                keys.remove(key)
            yield from property_schema.get_schema_errors(item, current_path)
        if keys and not self.additional_properties:
            yield SchemaError(current_path, 'additional_properties', ', '.join(keys))
