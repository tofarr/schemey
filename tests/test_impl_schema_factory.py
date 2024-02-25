from abc import abstractmethod, ABC
from dataclasses import dataclass
from unittest import TestCase

from injecty import create_injecty_context

from schemey import Schema
from schemey.schema_context import create_schema_context


@dataclass
class PetABC(ABC):
    name: str

    @abstractmethod
    def annunciate(self):
        """Make a noise!"""


class Dog(PetABC):
    def annunciate(self):
        return "Woof!"


class Cat(PetABC):
    def annunciate(self):
        return "Meow!"


class TestImplSchemaFactory(TestCase):
    @staticmethod
    def get_context():
        injecty_context = create_injecty_context()
        injecty_context.register_impls(PetABC, [Cat, Dog])
        schema_context = create_schema_context(injecty_context=injecty_context)
        return schema_context

    def test_pet_impl(self):
        context = self.get_context()
        schema = context.schema_from_type(PetABC)
        expected = Schema(
            {
                "name": "PetABC",
                "anyOf": [
                    {
                        "type": "array",
                        "prefixItems": [
                            {"const": "Cat"},
                            {
                                "type": "object",
                                "name": "Cat",
                                "properties": {"name": {"type": "string"}},
                                "additionalProperties": False,
                                "required": ["name"],
                            },
                        ],
                        "items": False,
                    },
                    {
                        "type": "array",
                        "prefixItems": [
                            {"const": "Dog"},
                            {
                                "type": "object",
                                "name": "Dog",
                                "properties": {"name": {"type": "string"}},
                                "additionalProperties": False,
                                "required": ["name"],
                            },
                        ],
                        "items": False,
                    },
                ],
            },
            PetABC,
        )
        self.assertEqual(expected, schema)

    def test_validate_pet(self):
        context = self.get_context()
        Dog("Bowser").annunciate()
        Cat("Garfield").annunciate()
        item = context.marshy_context.dump(Dog("Bowser"), PetABC)
        schema = context.schema_from_type(PetABC)
        schema.validate(item)

    def test_pet_from_json(self):
        context = self.get_context()
        expected = context.schema_from_type(PetABC)
        from_json = context.schema_from_json(expected.schema)
        self.assertEqual(expected, from_json)
