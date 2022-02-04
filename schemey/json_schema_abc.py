from abc import abstractmethod, ABC
from typing import Iterator, Optional, List, TypeVar

from marshy.types import ExternalItemType

from schemey.schema_error import SchemaError

T = TypeVar('T')
_JsonSchemaABC = f"{__name__}JsonSchemaABC"
_JsonSchemaContext = 'schemey.json_schema_context.JsonSchemaContext'


class NoDefault:
    pass


class JsonSchemaABC(ABC):
    """
    A Schema for a particular type of object, which may be marshalled into a JsonSchema. Json Schemas are fundamentally
    extensible and tolerant of additional unknown attributes. We use this to pass additional data to clients and store
    things that may not be part of the general spec.
    """

    @abstractmethod
    def get_schema_errors(self,
                          item: ExternalItemType,
                          current_path: Optional[List[str]] = None

                          ) -> Iterator[SchemaError]:
        """ Get the validation errors for the item given. """

    def validate(self, item: ExternalItemType, current_path: Optional[List[str]] = None):
        """ Validate the item given """
        errors = self.get_schema_errors(item, current_path)
        error = next(errors, None)
        if error:
            raise error

    @abstractmethod
    def dump_json_schema(self, json_context: _JsonSchemaContext) -> ExternalItemType:
        """ Convert this to a json schema """

    def simplify(self) -> _JsonSchemaABC:
        return self