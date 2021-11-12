from dataclasses import dataclass, field
from typing import Type, Dict, Set

from marshy import get_default_context
from marshy.marshaller_context import MarshallerContext
from marshy.types import ExternalItemType

REF = '$ref'
DEFS = '$defs'


@dataclass
class JsonOutputContext:
    marshaller_context: MarshallerContext = None
    defs: Dict[str, ExternalItemType] = field(default_factory=dict)
    item_types: Set[Type] = field(default_factory=set)

    def __post_init__(self):
        if self.marshaller_context is None:
            self.marshaller_context = get_default_context()

    def is_item_type_handled(self, item_type: Type) -> bool:
        return item_type in self.item_types

    def add_handled_item_type(self, item_type: Type):
        self.item_types.add(item_type)

    def add_def(self, name: str, json_schema: ExternalItemType):
        self.defs[name] = json_schema

    def to_json_schema(self, json_schema: ExternalItemType):
        if REF in json_schema and len(self.defs) == 1:
            return next(iter(self.defs.values()))
        return {DEFS: self.defs, 'allOf': [json_schema]}
