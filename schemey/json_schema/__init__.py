from typing import Callable, Dict

_custom_validators = {}


def register_custom_json_schema_validator(property_name: str, validator: Callable):
    _custom_validators[property_name] = validator


def get_custom_json_schema_validators() -> Dict[str, Callable]:
    return _custom_validators
