from typing import Optional

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.jsonifier.schema_jsonifier_abc import SchemaJsonifierABC
from schemey.string_schema import StringSchema
from schemey.string_format import StringFormat


class StringSchemaJsonifier(SchemaJsonifierABC):

    def load_schema(self, item: ExternalItemType, json_load: JsonLoad) -> Optional[JsonSchemaABC]:
        if item.get('type') != 'string':
            return None
        loaded = StringSchema(
            min_length=item.get('minLength'),
            max_length=item.get('maxLength'),
            pattern=item.get('pattern'),
            format=StringFormat(item.get('format')) if item.get('format') else None,
            default_value=item.get('default', NoDefault)
        )
        return loaded

    def dump_schema(self, item: JsonSchemaABC, json_dump: JsonDump) -> Optional[ExternalItemType]:
        if not isinstance(item, StringSchema):
            return None
        dumped = filter_none(dict(
            type='string',
            minLength=item.min_length,
            maxLength=item.max_length,
            pattern=item.pattern,
            format=item.format.value if item.format else None,
        ))
        if item.default_value is not NoDefault:
            dumped['default'] = item.default_value
        return dumped
