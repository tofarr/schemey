from dataclasses import dataclass
from typing import Optional

from schemey.validator import validator_from_type


@dataclass
class HelloWorld:
    name: str
    age: Optional[int] = None
    friend: Optional[bool] = None


# A validator may be generated...
validator = validator_from_type(HelloWorld)

# A full listing of errors for an item can be retrieved:
# noinspection PyTypeChecker
errors = list(
    validator.iter_errors(HelloWorld(None))
)  # [ValidationError("None is not of type 'string'")]

# ...or validation errors can be thrown:
validator.validate(HelloWorld("You"))  # No errors
# validator.validate(HelloWorld(None)) # raises ValidationError("None is not of type 'string'")
