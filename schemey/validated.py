from dataclasses import dataclass, fields
from typing import Optional, Type, TypeVar

from schemey import get_default_schema_context, SchemaContext, Schema

T = TypeVar("T")


class _ValidatingInstanceWrapper:
    def __init__(self, __wrapped__, __schemey_validators__):
        object.__setattr__(self, "__wrapped__", __wrapped__)
        object.__setattr__(self, "__schemey_validators__", __schemey_validators__)

    def __getattr__(self, item):
        wrapped = object.__getattribute__(self, "__wrapped__")
        return getattr(wrapped, item)

    def __setattr__(self, key, value):
        validators = object.__getattribute__(self, "__schemey_validators__")
        validator = validators.get(key)
        if validator:
            validator.validate(value)
        wrapped = object.__getattribute__(self, "__wrapped__")
        return setattr(wrapped, key, value)

    def __repr__(self):
        wrapped = object.__getattribute__(self, "__wrapped__")
        return wrapped.__repr__()

    def __eq__(self, other):
        wrapped = object.__getattribute__(self, "__wrapped__")
        if isinstance(other, _ValidatingInstanceWrapper):
            other = object.__getattribute__(other, "__wrapped__")
        return wrapped.__eq__(other)


class _ValidatingClassWrapper:
    def __init__(self, __wrapped__, __schemey_validators__=None):
        object.__setattr__(self, "__wrapped__", __wrapped__)
        object.__setattr__(self, "__schemey_validators__", __schemey_validators__)

    def __getattr__(self, item):
        wrapped = object.__getattribute__(self, "__wrapped__")
        return getattr(wrapped, item)

    def __call__(self, *args, **kwargs):
        wrapped_class = object.__getattribute__(self, "__wrapped__")
        to_wrap = wrapped_class.__call__(*args, **kwargs)
        validators = object.__getattribute__(self, "__schemey_validators__")
        for name, property_validator in validators.items():
            value = getattr(to_wrap, name)
            property_validator.validate(value)
        return _ValidatingInstanceWrapper(to_wrap, validators)


def validated(cls: Type[T], schema_context: Optional[SchemaContext] = None):
    if schema_context is None:
        schema_context = get_default_schema_context()

    def wrap(cls_):
        from schemey.validator import Validator

        type_ = dataclass(cls_)
        marshaller_context = schema_context.marshaller_context
        schema = schema_context.schema_from_type(type_)
        properties = schema.schema["properties"]
        validators = {}
        for field in fields(type_):
            prop = properties.get(field.name)
            if prop:
                schema = Schema(prop, field.type)
                marshaller = marshaller_context.get_marshaller(field.type)
                validators[field.name] = Validator(schema, marshaller)

        return _ValidatingClassWrapper(type_, validators)

    return wrap if cls is None else wrap(cls)
