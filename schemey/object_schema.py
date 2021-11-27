from dataclasses import dataclass, field
from typing import Iterable, Union, Sized, Optional, List, Iterator, Type

from marshy.types import ExternalItemType

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
        if keys:
            yield SchemaError(current_path, 'additional_attributes', ', '.join(keys))

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        local_json_output_context = json_output_context or JsonOutputContext()
        if not local_json_output_context.is_item_type_handled(self.item_type):
            local_json_output_context.add_handled_item_type(self.item_type)
            properties = {p.name: p.to_json_schema(local_json_output_context) for p in self.property_schemas}
            json_schema = dict(type=OBJECT, properties=properties, additionalProperties=False)
            if self.default_value is not None:
                json_schema['default'] = local_json_output_context.marshaller_context.dump(self.default_value)
            local_json_output_context.add_def(self.name, json_schema)
        json_schema = {REF: f'#$defs/{self.name}'}
        if json_output_context is None:
            json_schema = local_json_output_context.to_json_schema(json_schema)
        return json_schema
