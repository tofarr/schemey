from typing import Optional

from marshy.types import ExternalItemType

from schemey.loader.json_schema_loader_abc import JsonSchemaLoaderABC
from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.json_schema_context import JsonSchemaContext
from schemey.number_schema import NumberSchema


class NumberSchemaLoader(JsonSchemaLoaderABC):

    def load(self, item: ExternalItemType, json_context: JsonSchemaContext) -> Optional[JsonSchemaABC]:
        if item.get('type') != 'number':
            return None
        loaded = NumberSchema(
            minimum=item.get('minimum'),
            exclusive_minimum=item.get('exclusiveMinimum'),
            maximum=item.get('maximum'),
            exclusive_maximum=item.get('exclusiveMaximum'),
            default=item.get('default', NoDefault)
        )
        return loaded
