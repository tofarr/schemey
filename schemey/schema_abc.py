from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Iterator, Type

from schemey.schema_error import SchemaError

T = TypeVar('T')


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
        """ Get the type of item processed by this schemey """

    @property
    @abstractmethod
    def default_value(self) -> Optional[T]:
        """ The default value for this schemey """
