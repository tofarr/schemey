from dataclasses import dataclass
from typing import Any, Union, List


@dataclass(frozen=True)
class SchemaError(Exception):
    path: str
    code: str
    value: Any

    def __init__(self, path: Union[str, List[str]], code: str, value: Any = None):
        if not isinstance(path, str):
            path = "/".join(path or [])
        super().__init__(f':{code}:{path}:{value}')
        object.__setattr__(self, 'path', path)
        object.__setattr__(self, 'code', code)
        object.__setattr__(self, 'value', value)
