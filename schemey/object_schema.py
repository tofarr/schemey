import inspect
from dataclasses import dataclass, field
from typing import Iterable, Union, Sized, Optional, List, Iterator, Type, TextIO

from marshy.types import ExternalItemType

from schemey.graphql.graphql_attr import GraphqlAttr
from schemey.graphql_context import GraphqlContext, GraphqlObjectType
from schemey.json_output_context import JsonOutputContext, REF
from schemey.property_schema import PropertySchema
from schemey.schema_abc import SchemaABC, T
from schemey.schema_error import SchemaError

OBJECT = 'object'
PROPERTIES = 'properties'


@dataclass(frozen=True)
class ObjectSchema(SchemaABC[T]):
    _item_type: Type[T]
    property_schemas: Union[Iterable[PropertySchema], Sized] = field(default_factory=tuple)
    default_value: Optional[T] = None
    name: str = None
    additional_properties: bool = False

    @property
    def item_type(self):
        return self._item_type

    def __post_init__(self):
        if self.name is None:
            object.__setattr__(self, 'name', self.item_type.__name__)

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if hasattr(item, 'keys'):
            keys = item.keys()
        elif hasattr(item, '__dict__'):
            keys = (k for k in item.__dict__ if not k.startswith('_'))
        else:
            yield SchemaError(current_path, 'type', item)
            return
        keys = set(keys)
        for property_schema in (self.property_schemas or []):
            if property_schema.name in keys:
                keys.remove(property_schema.name)
            yield from property_schema.get_schema_errors(item, current_path)
        if keys and not self.additional_properties:
            yield SchemaError(current_path, 'additional_properties', ', '.join(keys))

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        local_json_output_context = json_output_context or JsonOutputContext()
        if not local_json_output_context.is_item_name_handled(self.name):
            local_json_output_context.set_def(self.name, {})
            properties = {p.name: p.to_json_schema(local_json_output_context) for p in self.property_schemas}
            json_schema = dict(type=OBJECT, properties=properties, additionalProperties=self.additional_properties)
            if self.default_value is not None:
                json_schema['default'] = local_json_output_context.marshaller_context.dump(self.default_value)
            local_json_output_context.set_def(self.name, json_schema)
        json_schema = {REF: f'#$defs/{self.name}'}
        if json_output_context is None:
            json_schema = local_json_output_context.to_json_schema(json_schema)
        return json_schema

    def to_graphql_schema(self, target: GraphqlContext):
        if self.name in target.objects:
            return
        target.objects[self.name] = self
        for property_schema in self.property_schemas:
            property_schema.schema.to_graphql_schema(target)

    def to_graphql(self, writer: TextIO, graphql_object_type: GraphqlObjectType):
        if not self._has_valid_attrs():
            return
        if self._has_real_doc_string():
            writer.write(f'"""\n{self.item_type.__doc__.strip()}\n"""\n')
        writer.write('%s %s {\n' % (graphql_object_type.value, self.name))
        for property_schema in self.property_schemas:
            graphql_attr = property_schema.to_graphql_attr()
            if graphql_attr:
                writer.write(f'\t{property_schema.name}: {graphql_attr.to_graphql()}\n')
        writer.write('}\n\n')

    def to_graphql_attr(self) -> Optional[GraphqlAttr]:
        if not self._has_valid_attrs():
            return
        return GraphqlAttr(self.name)

    def _has_valid_attrs(self):
        schemas = (s for s in self.property_schemas if s.to_graphql_attr())
        has_valid_attrs = next(schemas, None) is not None
        return has_valid_attrs

    def _has_real_doc_string(self):
        """
        The auto generated docstrings are useless in the context of graphql, so we include the docstring only
        if it has been customized
        """
        doc = self.item_type.__doc__
        if doc is None or self.item_type is dict:
            return False
        default_doc = self.item_type.__name__ + str(inspect.signature(self.item_type)).replace(' -> None', '')
        return default_doc != doc
