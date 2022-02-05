from dataclasses import dataclass
from typing import Optional, Type, List, Iterator, TypeVar

from marshy.marshaller.marshaller_abc import MarshallerABC

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
