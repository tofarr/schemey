from dataclasses import field, dataclass
from typing import Dict

from marshy.types import ExternalItemType, ExternalType

from schemey.json_schema_abc import JsonSchemaABC
from schemey.jsonifier.json_dump import get_element

_SchemeyContext = 'schemey.schemey_context.SchemeyContext'


@dataclass
class JsonLoad:
    schemey_context: _SchemeyContext
    root: ExternalItemType
    defs: Dict[str, JsonSchemaABC] = field(default_factory=dict)

    def get_element(self, ref: str) -> ExternalType:
        return get_element(self.root, ref)

    def load(self, item: ExternalItemType) -> JsonSchemaABC:
        loads = (jsonifier.load_schema(item, self) for jsonifier in self.schemey_context.schema_jsonifiers)
        loaded = next(d for d in loads if d is not None)
        return loaded
