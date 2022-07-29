from dataclasses import field, dataclass
from datetime import datetime
from uuid import UUID, uuid4

from schemey.schema import str_schema

from schemey.string_format import StringFormat
from schemey.validator import validator_from_type

# A validations are available out of the box for UUID, str, bool, int float, datetime, dataclasses, lists, tuples, sets
# and unions...


@dataclass
class User:
    email: str = field(
        metadata=dict(schemey=str_schema(str_format=StringFormat.EMAIL, max_length=255))
    )
    language_code: str = field(
        metadata=dict(schemey=str_schema(min_length=2, max_length=2, pattern="^\\w+$"))
    )
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)


validator = validator_from_type(User)
validator.validate(User(email="developer@developer.com", language_code="en"))
# validator.validate(User(email='not_an_email', language_code='en')) # raises ValidationError
