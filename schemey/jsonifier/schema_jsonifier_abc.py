from abc import ABC, abstractmethod
from functools import total_ordering
from typing import Optional

from marshy.types import ExternalItemType

from schemey.jsonifier.json_dump import JsonDump
from schemey.jsonifier.json_load import JsonLoad
from schemey.json_schema_abc import JsonSchemaABC


@total_ordering
class SchemaJsonifierABC(ABC):

    @property
    def priority(self) -> int:
        return 0

    def __ne__(self, other):
        return self.priority != getattr(other, 'priority', None)

    def __lt__(self, other):
        return self.priority < getattr(other, 'priority', None)

    @abstractmethod
    def load_schema(self, item: ExternalItemType, json_load: JsonLoad) -> Optional[JsonSchemaABC]:
        """ Load a schema - return None if not possible using this jsonifier """

    def dump_schema(self, item: JsonSchemaABC, json_dump: JsonDump) -> Optional[ExternalItemType]:
        """ Dump a schema - return None if not possible using this jsonifier """
