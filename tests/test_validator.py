from dataclasses import dataclass, field
from typing import Optional
from unittest import TestCase

from jsonschema import ValidationError

from schemey.schema import str_schema
from schemey.string_format import StringFormat
from schemey.validator import validator_from_type


@dataclass
class User:
    email: Optional[str] = field(
        default=None,
        metadata=dict(
            schemey=str_schema(str_format=StringFormat.EMAIL, max_length=255)
        ),
    )


class TestValidator(TestCase):
    def test_python_type(self):
        validator = validator_from_type(User)
        self.assertEqual(User, validator.python_type)

    def test_json_schema(self):
        validator = validator_from_type(User)
        expected_json_schema = {
            "type": "object",
            "name": "User",
            "properties": {
                "email": {
                    "type": "string",
                    "maxLength": 255,
                    "format": "email",
                    "default": None,
                }
            },
            "additionalProperties": False,
            "required": [],
            "description": "User(email: Union[str, NoneType] = None)",
        }
        self.assertEqual(expected_json_schema, validator.json_schema)

    def test_validated_type(self):
        validator = validator_from_type(User)
        # noinspection PyPep8Naming
        VUser = validator.validated_type
        with self.assertRaises(ValidationError):
            VUser("not_an_email")
        user = VUser("developer@developer.com")
        with self.assertRaises(ValidationError):
            user.email = "not_an_email"
        self.assertNotEqual(VUser, User)
        self.assertEqual("User", VUser.__name__)
        self.assertEqual(None, VUser.email)
        self.assertEqual(user, user)
        user2 = VUser("developer@developer.com")
        self.assertEqual(user, user2)
        user3 = VUser("another@developer.com")
        self.assertNotEqual(user, user3)
