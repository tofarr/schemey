from datetime import datetime
from uuid import uuid4

from schemey.validator import validator_from_json

# We can start off with a json schema and dynamically generate the class!
# (This process is pluggable)

json_schema = {
    "type": "object",
    "name": "User",
    "properties": {
        "email": {"type": "string", "maxLength": 255, "format": "email"},
        "language_code": {
            "type": "string",
            "minLength": 2,
            "maxLength": 2,
            "pattern": "^\\w+$",
        },
        "id": {"type": "string", "format": "uuid"},
        "created_at": {"type": "string", "format": "date-time"},
    },
    "additionalProperties": False,
    "required": ["email", "language_code"],
    "description": "A user object!",
}

validator = validator_from_json(json_schema)
# use "python_type" instead of "validated_type" for non validated
User = validator.validated_type
print(
    User(
        id=uuid4(),
        email="developer@developer.com",
        language_code="en",
        created_at=datetime.now(),
    )
)
