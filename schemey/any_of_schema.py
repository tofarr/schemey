from dataclasses import dataclass
from typing import Optional, List, Iterator, Iterable, Union, Sized

from marshy.types import ExternalType, ExternalItemType

from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class AnyOfSchema(SchemaABC):
    schemas: Union[Iterable[SchemaABC], Sized]
    name: str = None

    def __post_init__(self):
        schemas = []
        for s in self.schemas:
            if isinstance(s, AnyOfSchema):
                schemas.extend(s.schemas)
            else:
                schemas.append(s)
        object.__setattr__(self, 'schemas', tuple(schemas))

    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        errors = [SchemaError(current_path or [], 'type', item)]
        for schema in self.schemas:
            errors = list(schema.get_schema_errors(item, current_path))
            if not errors:
                return
        if item is not None:
            yield from errors

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        any_of = [s.dump_json_schema(json_context) for s in self.schemas]
        dumped = dict(anyOf=any_of)
        if self.name:
            dumped['name'] = self.name
        return dumped

    def simplify(self) -> SchemaABC:
        any_of = [s.simplify() for s in self.schemas]
        schema = AnyOfSchema(**{**self.__dict__, 'schemas': any_of})
        return schema
