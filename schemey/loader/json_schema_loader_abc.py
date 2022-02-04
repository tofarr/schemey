from abc import abstractmethod, ABC
from typing import Optional

from marshy.types import ExternalItemType

from schemey.json_schema_abc import JsonSchemaABC

_JsonSchemaContext = 'schemey.json_schema_context.JsonSchemaContext'


class JsonSchemaLoaderABC(ABC):

    @abstractmethod
    def load(self, item: ExternalItemType, json_context: _JsonSchemaContext) -> Optional[JsonSchemaABC]:
        """ Load a schema - return None if not possible using this jsonifier """

    @property
    def priority(self) -> int:
        return 0

    def __ne__(self, other):
        return self.priority != getattr(other, 'priority', None)

    def __lt__(self, other):
        return self.priority < getattr(other, 'priority', None)
