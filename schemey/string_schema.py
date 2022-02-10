from dataclasses import dataclass
from datetime import datetime, time
import re
from typing import Optional, List, Iterator, Dict, Any, Union, Type, Callable
from uuid import UUID

import validators
from marshy.types import ExternalItemType

from schemey._util import filter_none
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_error import SchemaError
from schemey.str_param_schema_abc import StrParamSchemaABC
from schemey.string_format import StringFormat


@dataclass(frozen=True)
class StringSchema(StrParamSchemaABC):
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    format: Optional[StringFormat] = None
    _compiled_pattern = None

    def __post_init__(self):
        object.__setattr__(self, '_compiled_pattern', None if self.pattern is None else re.compile(self.pattern))

    def get_schema_errors(self, item: str, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if not isinstance(item, str):
            yield SchemaError(current_path, 'type', item)
            return
        if self.min_length is not None and len(item) < self.min_length:
            yield SchemaError(current_path, 'min_length', item)
        if self.max_length is not None and len(item) > self.max_length:
            yield SchemaError(current_path, 'max_length', item)
        if self._compiled_pattern is not None and not self._compiled_pattern.search(item):
            yield SchemaError(current_path, 'pattern', item)
        if self.format == StringFormat.DATE:
            try:
                if datetime.fromisoformat(item).isoformat()[:10] != item:
                    yield SchemaError(current_path, 'format:date', item)
            except ValueError:
                yield SchemaError(current_path, 'format:date', item)
        elif self.format == StringFormat.DATE_TIME:
            try:
                datetime.fromisoformat(item).isoformat()
            except ValueError:
                yield SchemaError(current_path, 'format:date-time', item)
        elif self.format == StringFormat.EMAIL:
            if validators.email(item) is not True:
                yield SchemaError(current_path, 'format:email', item)
        elif self.format == StringFormat.HOSTNAME:
            if validators.domain(item) is not True:
                yield SchemaError(current_path, 'format:hostname', item)
        elif self.format == StringFormat.IPV4:
            if validators.ipv4(item) is not True:
                yield SchemaError(current_path, 'format:ipv4', item)
        elif self.format == StringFormat.IPV6:
            if validators.ipv6(item) is not True:
                yield SchemaError(current_path, 'format:ipv6', item)
        elif self.format == StringFormat.TIME:
            try:
                time.fromisoformat(item).isoformat()
            except ValueError:
                yield SchemaError(current_path, 'format:time', item)
        elif self.format == StringFormat.URI:
            if validators.url(item) is not True:
                yield SchemaError(current_path, 'format:uri', item)
        elif self.format == StringFormat.UUID:
            if validators.uuid(item) is not True:
                yield SchemaError(current_path, 'format:uuid', item)

    def dump_json_schema(self, json_context: JsonSchemaContext) -> ExternalItemType:
        dumped = filter_none(dict(
            type='string',
            minLength=self.min_length,
            maxLength=self.max_length,
            pattern=self.pattern,
            format=self.format.value if self.format else None,
        ))
        return dumped

    def get_normalized_type(self, existing_types: Dict[str, Any], obj_wrapper: Callable
                          ) -> Union[Type[str], Type[UUID], Type[datetime]]:
        if self.format == StringFormat.DATE_TIME:
            return datetime
        elif self.format == StringFormat.UUID:
            return UUID
        return str
