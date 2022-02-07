import copy
from dataclasses import dataclass, MISSING
from typing import Optional, List, Iterator, Union, Type, Tuple, Dict

from marshy import ExternalType
from marshy.types import ExternalItemType

from schemey.param_schema import ParamSchema
from schemey.schema_abc import SchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass
class OptionalSchema(SchemaABC):
    """
    Attributes can be optional or required. ObjectSchemas contain a list of required property names,
    and all other properties should be Optional - and may have a default value (NoDefault is used
    for dynamic defaults - e.g.: field(default_factory=uuid4)
    """
    schema: SchemaABC
    default: Union[ExternalType, Type[NoDefault]] = NoDefault

    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if item is not None and item is not MISSING:
            yield from self.schema.get_schema_errors(item, current_path)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        schema = self.schema.dump_json_schema(json_context)
        if self.default is not NoDefault:
            schema['default'] = copy.deepcopy(self.default)
        return schema

    def simplify(self) -> SchemaABC:
        schema = OptionalSchema(self.schema.simplify(), self.default)
        return schema

    def get_param_schemas(self, current_path: str) -> Optional[List[ParamSchema]]:
        """ Optional schemas allow only one parameter """
        schemas = self.schema.get_param_schemas(current_path)
        if schemas and len(schemas) == 1:
            schemas[0].required = False
            return schemas

    def from_url_params(self, current_path: str, params: Dict[str, List[str]]) -> ExternalType:
        params = self.schema.from_url_params(current_path, params)
        if params is NoDefault:
            if self.default is NoDefault:
                params = None
            else:
                params = copy.deepcopy(self.default)
        return params

    def to_url_params(self, current_path: str, item: ExternalType) -> Iterator[Tuple[str, str]]:
        yield from self.schema.to_url_params(current_path, item)
