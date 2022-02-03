from dataclasses import dataclass, field
from typing import Type

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC, T

from schemey.json_schema_abc import JsonSchemaABC
from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.schemey_context import SchemeyContext, get_default_schemey_context


@dataclass
class JsonSchemaMarshaller(MarshallerABC[JsonSchemaABC]):
    marshalled_type: Type[JsonSchemaABC] = JsonSchemaABC
    schemey_context: SchemeyContext = field(default_factory=get_default_schemey_context)

    def load(self, item: ExternalType) -> JsonSchemaABC:
        json_load = JsonLoad(self.schemey_context)
        for schema_jsonifier in self.schemey_context.schema_jsonifiers:
            schema = schema_jsonifier.load_schema(item, json_load)
            if schema:
                return schema
        raise ValueError(f'load_faild:{item}')

    def dump(self, item: T) -> ExternalType:
        json_dump = JsonDump(self.schemey_context)
        for schema_jsonifier in self.schemey_context.schema_jsonifiers:
            schema = schema_jsonifier.dump_schema(item, json_dump)
            if schema:
                return schema
        raise ValueError(f'dump_failed:{item}')
