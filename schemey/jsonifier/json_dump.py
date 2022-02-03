from dataclasses import field, dataclass
from typing import Dict

from marshy.types import ExternalItemType, ExternalType

from schemey.json_schema_abc import JsonSchemaABC

_SchemeyContext = 'schemey.schemey_context.SchemeyContext'


@dataclass(frozen=True)
class JsonDump:
    schemey_context: _SchemeyContext
    root: ExternalItemType = field(default_factory=dict)
    defs_path: str = '#$defs'
    num_refs: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        assert self.defs_path.startswith('#')
        element = self.root
        for key in self.defs_path[1:].split('/'):
            if key not in element:
                element[key] = {}
            element = element[key]

    def get_element(self, ref: str) -> ExternalType:
        return get_element(self.root, ref)

    def dump(self, schema: JsonSchemaABC) -> ExternalItemType:
        dumps = (jsonifier.dump_schema(schema, self) for jsonifier in self.schemey_context.schema_jsonifiers)
        dumped = next(d for d in dumps if d is not None)
        return dumped


def get_element(root, ref: str) -> ExternalType:
    assert ref.startswith('#')
    element = root
    for key in ref[1:].split('/'):
        element = element[key]
    return element
