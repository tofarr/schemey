from abc import ABC, abstractmethod


# pylint: disable=R0903
class SchemaValidatorABC(ABC):
    property_name: str

    @abstractmethod
    def validate(self, validator, aP, instance, schema):
        """Validate this property"""
