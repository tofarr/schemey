from dataclasses import dataclass
from datetime import datetime
from typing import Type, Iterator, Optional, Union
from uuid import UUID

from jsonschema import ValidationError
from jsonschema.validators import validator_for
from marshy.types import ExternalItemType, ExternalType

from schemey.schemey_format_checker import SchemeyFormatChecker
from schemey.string_format import StringFormat
from schemey.util import filter_none


@dataclass
class Schema:
    schema: ExternalItemType
    python_type: Type

    def validator(self):
        validator = validator_for(self.schema)(
            schema=self.schema, format_checker=SchemeyFormatChecker()
        )
        return validator

    def iter_errors(self, item: ExternalType) -> Iterator[ValidationError]:
        yield from self.validator().iter_errors(instance=item)

    def validate(self, item: ExternalType):
        self.validator().validate(instance=item)


def str_schema(
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    str_format: Union[type(None), str, StringFormat] = None,
    pattern: Optional[str] = None,
) -> Schema:
    if isinstance(str_format, str):
        str_format = StringFormat(str_format)
    if str_format:
        str_format = str_format.value
    return Schema(
        filter_none(
            {
                "type": "string",
                "minLength": min_length,
                "maxLength": max_length,
                "format": str_format,
                "pattern": pattern,
            }
        ),
        str,
    )


def int_schema(
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    exclusive_minimum: Optional[int] = None,
    exclusive_maximum: Optional[int] = None,
) -> Schema:
    return Schema(
        filter_none(
            {
                "type": "integer",
                "minimum": minimum,
                "maximum": maximum,
                "exclusiveMinimum": exclusive_minimum,
                "exclusiveMaximum": exclusive_maximum,
            }
        ),
        int,
    )


def float_schema(
    minimum: Optional[float] = None,
    maximum: Optional[float] = None,
    exclusive_minimum: Optional[float] = None,
    exclusive_maximum: Optional[float] = None,
) -> Schema:
    return Schema(
        filter_none(
            {
                "type": "number",
                "minimum": minimum,
                "maximum": maximum,
                "exclusiveMinimum": exclusive_minimum,
                "exclusiveMaximum": exclusive_maximum,
            }
        ),
        float,
    )


def uuid_schema():
    return Schema({"type": "string", "format": "uuid"}, UUID)


def datetime_schema():
    return Schema({"type": "string", "format": "date-time"}, datetime)


def update_refs(schema: ExternalType, from_location: str, to_location: str):
    """Swap a referenced schema from one location to another"""
    if isinstance(schema, dict):
        schema = {
            k: update_refs(s, from_location, to_location) for k, s in schema.items()
        }
        ref = schema.get("$ref")
        if ref == from_location:
            schema["$ref"] = to_location
    elif isinstance(schema, list):
        return [update_refs(s, from_location, to_location) for s in schema]
    return schema
