from dataclasses import dataclass, MISSING
from typing import Optional, Type, List, Iterator, TypeVar, Dict, Union, Tuple

from marshy import ExternalType
from marshy.marshaller.marshaller_abc import MarshallerABC

from schemey.optional_schema import NoDefault
from schemey.param_schema import ParamSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError

T = TypeVar("T")


@dataclass
class ObjSchema:
    """Implementation of SchemaABC using Json"""

    json_schema: SchemaABC
    marshaller: MarshallerABC[T]

    def get_schema_errors(
        self, item: T, current_path: Optional[List[str]] = None
    ) -> Iterator[SchemaError]:
        try:
            dumped = self.marshaller.dump(item)
        except (ValueError, AttributeError):
            yield SchemaError(current_path, "type", item)
            return
        yield from self.json_schema.get_schema_errors(dumped, current_path)

    @property
    def item_type(self) -> Type[T]:
        return self.marshaller.marshalled_type

    def validate(self, item: T, current_path: Optional[List[str]] = None):
        """Validate the item given"""
        errors = self.get_schema_errors(item, current_path)
        error = next(errors, None)
        if error:
            raise error

    def get_param_schemas(self, current_path: str = "") -> Optional[List[ParamSchema]]:
        """Optional schemas allow only one parameter"""
        return self.json_schema.get_param_schemas(current_path)

    def from_url_params(
        self, params: Dict[str, List[str]], current_path: str = ""
    ) -> Union[ExternalType, NoDefault]:
        item = self.json_schema.from_url_params(current_path, params)
        if item is MISSING:
            return None
        elif item is NoDefault:
            raise ValueError("missing_required_fields")
        loaded = self.marshaller.load(item)
        return loaded

    def to_url_params(
        self, item: T, current_path: str = ""
    ) -> Iterator[Tuple[str, str]]:
        dumped = self.marshaller.dump(item)
        yield from self.json_schema.to_url_params(current_path, dumped)
