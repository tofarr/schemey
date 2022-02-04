from abc import abstractmethod, ABC
from functools import total_ordering
from typing import TypeVar, Type, Optional, Union

from marshy import ExternalType

from schemey.json_schema_abc import JsonSchemaABC, NoDefault

T = TypeVar('T')
NONE_TYPE = type(None)
_JsonSchemaContext = 'schemey.json_schema_context.JsonSchemaContext'


@total_ordering
class JsonSchemaFactoryABC(ABC):

    @property
    def priority(self):
        return 100

    @abstractmethod
    def create(self,
               type_: Type,
               json_context: _JsonSchemaContext,
               default: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        """
        Create a schema for the type given, or return None if that was not possible
        """

    def __ne__(self, other):
        return self.priority != getattr(other, 'priority', None)

    def __lt__(self, other):
        return self.priority < getattr(other, 'priority', None)
