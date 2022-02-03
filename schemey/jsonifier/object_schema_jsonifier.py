from typing import Optional

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.jsonifier.schema_jsonifier_abc import SchemaJsonifierABC
from schemey.object_schema import ObjectSchema


class ObjectSchemaJsonifier(SchemaJsonifierABC):

    def load_schema(self, item: ExternalItemType, json_load: JsonLoad) -> Optional[JsonSchemaABC]:
        if item.get('type') != 'object':
            return None
        name = item.get('name')
        properties = item.get('properties') or {}
        properties = {k: json_load.load(s) for k, s in properties.items()}
        loaded = ObjectSchema(
            name=name,
            properties=properties,
            additional_properties=item.get('additional_properties'),
            required=item.get('required')
        )
        return loaded

    def dump_schema(self, item: JsonSchemaABC, json_dump: JsonDump) -> Optional[ExternalItemType]:
        if not isinstance(item, ObjectSchema):
            return None
        dumped = filter_none(dict(
            type='object',
            name=item.name,
            additional_properties=item.additional_properties
        ))
        properties = {k: json_dump.dump(s) for k, s in item.properties.items()}
        if properties:
            dumped['properties'] = properties
        if item.required:
            dumped['required'] = item.required
        if item.default_value is not NoDefault:
            dumped['default'] = item.default_value
        return dumped
