from typing import Optional

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.any_of_schema import AnyOfSchema
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.jsonifier.schema_jsonifier_abc import SchemaJsonifierABC


class AnyOfSchemaJsonifier(SchemaJsonifierABC):

    def load_schema(self, item: ExternalItemType, json_load: JsonLoad) -> Optional[JsonSchemaABC]:
        any_of = item.get('anyOf')
        if any_of is None:
            return
        schemas = [json_load.load(a) for a in any_of]
        loaded = AnyOfSchema(**filter_none(dict(
            schemas=schemas,
            name=item.get('name'),
            default_value=item.get('default', NoDefault)
        )))
        return loaded

    def dump_schema(self, item: JsonSchemaABC, json_dump: JsonDump) -> Optional[ExternalItemType]:
        if not isinstance(item, AnyOfSchema):
            return None
        any_of = [json_dump.dump(s) for s in item.schemas]
        dumped = filter_none(dict(
            anyOf=any_of,
            name=item.name
        ))
        if item.default_value is not NoDefault:
            dumped['default'] = item.default_value
        return dumped
