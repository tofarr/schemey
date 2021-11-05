from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.marshaller.schema_marshaller import TYPE
from schemey.marshaller.schema_marshaller_abc import SchemaMarshallerABC
from schemey.marshaller.util import filter_none
from schemey.string_schema import StringSchema

STRING = 'string'
FORMAT = 'format'


class StringSchemaMarshaller(SchemaMarshallerABC[StringSchema]):

    def __init__(self):
        super().__init__(StringSchema)

    def can_load(self, item: ExternalItemType) -> bool:
        return item.get(TYPE) == STRING

    def load(self, item: ExternalType) -> StringSchema:
        return StringSchema(
            min_length=int(item['minLength']) if hasattr(item, 'minLength') else None,
            max_length=int(item['maxLength']) if hasattr(item, 'maxLength') else None,
            pattern=item.get('pattern'),
            format=item.get('format')
        )

    def dump(self, schema: StringSchema) -> ExternalType:
        return filter_none(dict(
            type='string',
            minLength=schema.min_length,
            maxLength=schema.max_length,
            pattern=schema.pattern,
            format=schema.format
        ))
