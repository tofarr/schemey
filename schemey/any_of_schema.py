from dataclasses import dataclass
from typing import Optional, List, Iterator, Iterable, Union, TextIO, Sized

from marshy.types import ExternalItemType

from schemey.graphql.graphql_attr import GraphqlAttr
from schemey.graphql_context import GraphqlContext
from schemey.json_output_context import JsonOutputContext, REF
from schemey.null_schema import NullSchema
from schemey.schema_abc import SchemaABC, T
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class AnyOfSchema(SchemaABC[T]):
    schemas: Union[Iterable[SchemaABC], Sized]
    default_value: Optional[T] = None
    name: str = None

    def __post_init__(self):
        schemas = []
        for s in self.schemas:
            if isinstance(s, AnyOfSchema):
                schemas.extend(s.schemas)
            else:
                schemas.append(s)
        object.__setattr__(self, 'schemas', tuple(schemas))

    @property
    def item_type(self):
        types = tuple(s.item_type for s in self.schemas)
        return Union[types]

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        errors = [SchemaError(current_path or [], 'type', item)]
        for schema in self.schemas:
            errors = list(schema.get_schema_errors(item, current_path))
            if not errors:
                return
        if item is not None:
            yield from errors

    def _get_json_name(self):
        if self.name:
            return self.name
        return f"AnyOf{''.join(self._get_type_names())}"

    def _get_type_names(self):
        for s in self.schemas:
            if isinstance(s, NullSchema):
                yield 'Null'
            else:
                graphql_attr = s.to_graphql_attr()
                if graphql_attr:
                    yield graphql_attr.type_name

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        name = self._get_json_name()
        local_json_output_context = json_output_context or JsonOutputContext()
        if not local_json_output_context.is_item_name_handled(name):
            local_json_output_context.set_def(name, {})
            json_schema = dict(anyOf=[s.to_json_schema(json_output_context) for s in self.schemas])
            if self.default_value is not None:
                json_schema['default'] = local_json_output_context.marshaller_context.dump(self.default_value)
            local_json_output_context.set_def(name, json_schema)
        json_schema = {REF: f'#$defs/{name}'}
        if json_output_context is None:
            json_schema = local_json_output_context.to_json_schema(json_schema)
        return json_schema

    def _get_graphql_name(self):
        if self.name:
            return self.name
        return f"AnyOf{''.join(n for n in self._get_type_names() if n != 'Null')}"

    def to_graphql_schema(self, target: GraphqlContext):
        schemas = [s for s in self.schemas if s != NullSchema() and s.to_graphql_attr()]
        num_schemas = len(schemas)
        if num_schemas == 0:
            return
        if num_schemas > 1:
            target.unions[self._get_graphql_name()] = self
        for schema in self.schemas:
            schema.to_graphql_schema(target)

    def to_graphql_attr(self) -> Optional[GraphqlAttr]:
        graphql_attrs = [s.to_graphql_attr() for s in self.schemas if s.to_graphql_attr()]
        num_attrs = len(graphql_attrs)
        if num_attrs == 0:
            return None
        if num_attrs == 1:
            graphql_attr = graphql_attrs[0]
        else:
            graphql_attr = GraphqlAttr(self._get_graphql_name())
        graphql_attr.required = next((False for s in self.schemas if isinstance(s, NullSchema)), True)
        return graphql_attr

    def to_graphql(self, writer: TextIO):
        graphql_attrs = (s.to_graphql_attr() for s in self.schemas)
        graphql_attrs = [g for g in graphql_attrs if g]
        if len(graphql_attrs) > 1:
            types = ' | '.join(g.type_name for g in graphql_attrs)
            writer.write(f"union {self._get_graphql_name()} = {types}\n")


def optional_schema(schema: SchemaABC) -> SchemaABC:
    return AnyOfSchema((NullSchema(), schema))


def strip_optional(schema: SchemaABC) -> SchemaABC:
    if not isinstance(schema, AnyOfSchema):
        return schema
    schemas = list(schema.schemas)
    if len(schemas) != 2:
        return schema
    if isinstance(schemas[0], NullSchema):
        return schemas[1]
    if isinstance(schemas[1], NullSchema):
        return schemas[0]
    return schema
