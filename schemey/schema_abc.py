from abc import abstractmethod, ABC
from typing import Iterator, Optional, List, TypeVar, Dict, Tuple, Union

from marshy.types import ExternalItemType, ExternalType

from schemey.schema_error import SchemaError

T = TypeVar('T')
_SchemaABC = f"{__name__}SchemaABC"
_JsonSchemaContext = 'schemey.json_schema_context.JsonSchemaContext'
_ParamSchema = 'schemey.param_schema.ParamSchema'


class NoDefault:
    pass


class SchemaABC(ABC):
    """
    A Schema for a particular type of object, which may be marshalled into a JsonSchema. Json Schemas are fundamentally
    extensible and tolerant of additional unknown attributes. We use this to pass additional data to clients and store
    things that may not be part of the general spec.
    """

    @abstractmethod
    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        """ Get the validation errors for the item given. """

    def validate(self, item: ExternalType, current_path: Optional[List[str]] = None):
        """ Validate the item given """
        errors = self.get_schema_errors(item, current_path)
        error = next(errors, None)
        if error:
            raise error

    @abstractmethod
    def dump_json_schema(self, json_context: _JsonSchemaContext) -> ExternalItemType:
        """ Convert this to a json schema """

    def simplify(self) -> _SchemaABC:
        return self

    def get_param_schemas(self, current_path: str) -> Optional[List[_ParamSchema]]:
        """
        Get OpenAPI json schemas for this schema. Not all schemas can be processed as url parameters
        some more complicated schemas are better processed as json input, and will return None
        """
        return None

    def from_url_params(self, current_path: str, params: Dict[str, List[str]]) -> Union[ExternalType, NoDefault]:
        """ Convert the url params given to a json item. Raise NotImplemented if get_param_schema is none. """
        raise NotImplemented

    def to_url_params(self, current_path: str, item: ExternalType) -> Iterator[Tuple[str, str]]:
        """ Convert the item given to url params Raise NotImplemented if get_param_schema is none. """
        raise NotImplemented
