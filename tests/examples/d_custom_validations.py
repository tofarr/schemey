from dataclasses import dataclass

from schemey import SchemaContext, Schema
from schemey.validator import validator_from_type


# Custom validations are supported - it's all just json schema!
# Below we make sure that the user is not named 'Bill' or 'Ted'


@dataclass
class User:
    name: str = ""

    @classmethod
    def __schema_factory__(cls, context: SchemaContext, path: str):
        return Schema(
            {
                "type": "object",
                "properties": {"name": {"not": {"enum": ["Bill", "Ted"]}}},
                "additionalProperties": False,
            },
            User,
        )


validator = validator_from_type(User)
validator.validate(User(name="Theodore"))  # :)
# validator.validate(User(name="Ted")) # raises ValidationError
