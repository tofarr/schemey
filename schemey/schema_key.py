from dataclasses import dataclass
from typing import Generic, Type, Optional, TypeVar

T = TypeVar('T')


@dataclass(frozen=True)
class SchemaKey(Generic[T]):
    type: Type[T]
    default_value: Optional[T]
