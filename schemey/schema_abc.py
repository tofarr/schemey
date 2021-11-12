from abc import abstractmethod, ABC
from typing import Iterator, Optional, List, Generic, TypeVar, Type

from marshy.types import ExternalItemType

from schemey.json_output_context import JsonOutputContext
from schemey.schema_error import SchemaError

T = TypeVar('T')
_SchemaABC = f'{__name__}.SchemaABC'


class SchemaABC(ABC, Generic[T]):
    """
    A Schema for a particular type of object, which may be marshalled into a JsonSchema. Json Schemas are fundamentally
    extensible and tolerant of additional unknown attributes. We use this to pass additional data to clients and store
    things that may not be part of the general spec.
    """

    @abstractmethod
    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        """ Get the validation errors for the item given. """

    def validate(self, item: T, current_path: Optional[List[str]] = None):
        """ Validate the item given """
        errors = self.get_schema_errors(item, current_path)
        error = next(errors, None)
        if error:
            raise error

    @property
    @abstractmethod
    def item_type(self) -> Type[T]:
        """ Get the type of item processed by this schema """

    @property
    @abstractmethod
    def default_value(self) -> Optional[T]:
        """ The default value for this schema """

    @abstractmethod
    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        """ Convert this schema to a json schema """
