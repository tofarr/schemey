from dataclasses import dataclass
from typing import Optional, Type, List, Iterator, TypeVar, Dict, Union, Tuple

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC

from schemey.optional_schema import NoDefault
from schemey.param_schema import ParamSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError

T = TypeVar('T')


@dataclass
class ObjSchema:
    """ Implementation of SchemaABC using Json """
    json_schema: SchemaABC
    marshaller: MarshallerABC[T]

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        try:
            dumped = self.marshaller.dump(item)
        except (ValueError, AttributeError):
            yield SchemaError(current_path, 'type', item)
            return
        yield from self.json_schema.get_schema_errors(dumped, current_path)

    @property
    def item_type(self) -> Type[T]:
        return self.marshaller.marshalled_type

    def validate(self, item: T, current_path: Optional[List[str]] = None):
        """ Validate the item given """
        errors = self.get_schema_errors(item, current_path)
        error = next(errors, None)
        if error:
            raise error

    def get_param_schemas(self, current_path: str) -> Optional[List[ParamSchema]]:
        """ Optional schemas allow only one parameter """
        return self.json_schema.get_param_schemas(current_path)

    def from_url_params(self, current_path: str, params: Dict[str, List[str]]) -> Union[ExternalType, NoDefault]:
        return self.json_schema.from_url_params(current_path, params)

    def to_url_params(self, current_path: str, item: ExternalType) -> Iterator[Tuple[str, str]]:
        yield from self.json_schema.to_url_params(current_path, item)
