from abc import abstractmethod, ABC
from dataclasses import dataclass
from unittest import TestCase

from marshy.factory.impl_marshaller_factory import register_impl

from schemey.schemey_context import schema_for_type


class PetAbc(ABC):
    @abstractmethod
    def annunciate(self):
        """ Introduce yourself! """


@dataclass
class Dog(PetAbc):
    num_legs: int = 4

    def annunciate(self):
        return "Woof!"


@dataclass
class Parrot(PetAbc):
    num_wings: int = 2

    def annunciate(self):
        return f"Kaw!"


register_impl(PetAbc, Dog)
register_impl(PetAbc, Parrot)


class TestImplSchema(TestCase):

    def test_impl(self):
        schema = schema_for_type(PetAbc)
        Dog().annunciate()
        Parrot().annunciate()
        self.assertEqual([], list(schema.get_schema_errors(Dog())))
        self.assertEqual([], list(schema.get_schema_errors(Parrot())))
