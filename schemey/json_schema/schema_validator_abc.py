from abc import ABC


class SchemaValidatorABC(ABC):
    property_name: str

    def validate(self, validator, aP, instance, schema):
        """Validate this property"""
