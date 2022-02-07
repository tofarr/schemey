from dataclasses import dataclass, MISSING
from typing import Optional, List, Iterator, Tuple, Dict, Union

from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.optional_schema import NoDefault
from schemey.param_schema import ParamSchema
from schemey.schema_abc import SchemaABC, _JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass
class TupleSchema(SchemaABC):
    schemas: Tuple[SchemaABC, ...]

    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if current_path is None:
            current_path = []
        if not isinstance(item, list) or len(item) != len(self.schemas):
            yield SchemaError(current_path, 'type', item)
            return
        for index, sub_item in enumerate(item):
            current_path.append(str(index))
            schema = self.schemas[index]
            yield from schema.get_schema_errors(sub_item, current_path)
            current_path.pop()

    def dump_json_schema(self, json_context: _JsonSchemaContext) -> ExternalItemType:
        schema = {
            "type": "array",
            "prefixItems": [i.dump_json_schema(json_context) for i in self.schemas],
            "items": False
        }
        return schema

    def get_param_schemas(self, current_path: str) -> Optional[List[ParamSchema]]:
        param_schemas = []
        for index, schema in enumerate(self.schemas):
            sub_schemas = schema.get_param_schemas(f"{current_path}.{index}")
            if sub_schemas is None:
                return None
            param_schemas.extend(sub_schemas)
        return param_schemas

    def from_url_params(self, current_path: str, params: Dict[str, List[str]]) -> ExternalType:
        values = []
        for index, schema in enumerate(self.schemas):
            sub_path = self._sub_path(current_path, index)
            value = schema.from_url_params(sub_path, params)
            if value is NoDefault:
                raise SchemaError(current_path, 'missing_value')
            values.append(value)
        return values

    def to_url_params(self, current_path: str, item: ExternalType) -> Iterator[Tuple[str, str]]:
        for index, schema in enumerate(self.schemas):
            sub_path = self._sub_path(current_path, index)
            yield from schema.to_url_params(sub_path, item[index])

    def _sub_path(self, current_path: str, index: int):
        sub_path = f"{current_path}.{index}" if current_path else str(index)
        return sub_path
