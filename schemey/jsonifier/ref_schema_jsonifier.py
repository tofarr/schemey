from typing import Optional
from uuid import uuid4

from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC
from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.jsonifier.schema_jsonifier_abc import SchemaJsonifierABC
from schemey.ref_schema import RefSchema


class RefSchemaJsonifier(SchemaJsonifierABC):

    def load_schema(self, item: ExternalItemType, json_load: JsonLoad) -> Optional[JsonSchemaABC]:
        if '$ref' not in item:
            return None
        ref = item['$ref']
        if ref in json_load.defs:
            return json_load.defs[ref]
        schema = RefSchema(ref)
        json_load.defs[ref] = schema
        referenced_item = json_load.get_element(ref)
        referenced_schema = json_load.load(referenced_item)
        schema.schema = referenced_schema
        return schema

    def dump_schema(self, item: RefSchema, json_dump: JsonDump) -> Optional[ExternalItemType]:
        if not isinstance(item, RefSchema):
            return None
        name = item.schema.name if hasattr(item.schema, 'name') else str(uuid4())
        defs = json_dump.get_element(json_dump.defs_path)
        if name not in defs:
            defs[name] = json_dump.dump(item.schema)
            json_dump.num_refs[name] = 0
        json_dump.num_refs[name] += 1
        return {'$ref': name}

