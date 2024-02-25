from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class SchemaValidatorABC(ABC):
    property_name: str

    def validate(self, validator, aP, instance, schema):
        """Validate this property"""
