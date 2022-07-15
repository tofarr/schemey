from abc import ABC
from typing import List, Union, Dict, Iterator, Tuple

from marshy import ExternalType

from schemey.optional_schema import NoDefault
from schemey.param_schema import ParamSchema
from schemey.schema_abc import SchemaABC


class StrParamSchemaABC(SchemaABC, ABC):
    def get_param_schemas(self, current_path: str) -> List[ParamSchema]:
        return [ParamSchema(name=current_path, schema=self)]

    def from_url_params(
        self, current_path: str, params: Dict[str, List[str]]
    ) -> Union[ExternalType, NoDefault]:
        if current_path not in params:
            return NoDefault
        values = params.get(current_path)
        return values[0]

    def to_url_params(self, current_path: str, item: str) -> Iterator[Tuple[str, str]]:
        yield current_path, str(item)
