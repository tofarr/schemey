from dataclasses import dataclass
from typing import Optional

from schemey.schema_context import schema_for_type


@dataclass
class HelloWorld:
    name: str
    age: Optional[int] = None
    friend: Optional[bool] = None


# A schema may be generated...
schema = schema_for_type(HelloWorld)

# A full listing of errors for an item can be retrieved:
# noinspection PyTypeChecker
errors = list(
    schema.get_schema_errors(HelloWorld(None))
)  # [SchemaError(path='name', code='type', value='You')]

# ...or validation errors can be thrown:
schema.validate(HelloWorld("You"))  # No errors
# schema.validate(HelloWorld(None)) # raises SchemaError(path='name', code='type', value=None)
