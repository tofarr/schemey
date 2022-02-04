from typing import Optional

from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.any_of_schema import AnyOfSchema
from schemey.loader.json_schema_loader_abc import JsonSchemaLoaderABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext


class AnyOfSchemaLoader(JsonSchemaLoaderABC):

    def load(self, item: ExternalItemType, json_context: JsonSchemaContext) -> Optional[JsonSchemaABC]:
        any_of = item.get('anyOf')
        if any_of is None:
            return
        schemas = [json_context.load(a) for a in any_of]
        loaded = AnyOfSchema(**dict(
            schemas=schemas,
            name=item.get('name'),
            default=item.get('default', NoDefault)
        ))
        return loaded
