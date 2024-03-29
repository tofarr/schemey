from dataclasses import dataclass, field
from typing import Generic, TypeVar, Iterator, Optional, Type

from injecty import InjectyContext, get_default_injecty_context
from jsonschema import ValidationError
from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey import Schema, SchemaContext, get_default_schema_context
from schemey.validated import validated

T = TypeVar("T")


@dataclass
class Validator(Generic[T]):
    schema: Schema
    marshaller: MarshallerABC[T]
    injecty_context: InjectyContext = field(default_factory=get_default_injecty_context)

    def iter_errors(self, obj: T) -> Iterator[ValidationError]:
        item = self.marshaller.dump(obj)
        yield from self.schema.iter_errors(item)

    def validate(self, obj: T):
        item = self.marshaller.dump(obj)
        self.schema.validate(item, self.injecty_context)

    @property
    def json_schema(self) -> ExternalItemType:
        return self.schema.schema

    @property
    def python_type(self) -> Type[T]:
        # noinspection PyTypeChecker
        return self.schema.python_type

    @property
    def validated_type(self) -> Type[T]:
        # noinspection PyTypeChecker
        return validated(self.schema.python_type)


def validator_from_type(type_, context: Optional[SchemaContext] = None) -> Validator:
    if context is None:
        context = get_default_schema_context()
    return Validator(
        schema=context.schema_from_type(type_),
        marshaller=context.marshy_context.get_marshaller(type_),
    )


def validator_from_json(
    item: ExternalItemType, context: Optional[SchemaContext] = None
) -> Validator:
    if context is None:
        context = get_default_schema_context()
    schema = context.schema_from_json(item)
    # noinspection PyTypeChecker
    return Validator(
        schema=schema,
        marshaller=context.marshy_context.get_marshaller(schema.python_type),
        injecty_context=context.marshy_context.injecty_context,
    )
