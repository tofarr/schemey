from dataclasses import dataclass, field
from typing import Optional
from schemey.number_schema import NumberSchema
from schemey.schema_context import schema_for_type


@dataclass
class Person:
    name: str
    age: Optional[int] = field(
        default=None, metadata=dict(schemey=NumberSchema(minimum=0))
    )


schema = schema_for_type(Person)

errors = list(
    schema.get_schema_errors(Person("You", -1))
)  # [SchemaError(path='age', code='minimum', value=-1)]
