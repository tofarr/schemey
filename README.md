# Schemey - Json Schemas for Python.

This project allows for generation of json schemas based on python
classes, or python classes based on json schemas. It also allows for
generation of validated dataclasses, where setters cannot violate
the invariants established in a schema.

It uses the fantastic [JSON Schema](https://github.com/python-jsonschema/jsonschema)
library for python. (Though older versions did not.)

The general idea is that the framework should not insist on any particular
data structure or paradigm - it is designed to be extensible, and out of the box support
is provided for iterable types, dataclasses, enums, timestamps and primitives.

Serialization is provided using marshy.

Current test coverage is at 100%

## Why did you build this?

There were gaps in the functionality of existing solutions (Like pydantic)
that made using them untenable for my use cases.

## Installation

`pip install schemey`

## Concepts

* A [Schema](schemey/schema.py) contains a link between a JSON Schema and a Python Type
* A [Validator](schemey/validator.py) is used to validate python objects using a schema
* A [SchemaContext](schemey/schema_context.py) is used to generate python objects for json schemas / vice versa
* A [SchemaFactory](schemey/factory/schema_factory_abc.py) is used to plug new translation rules into a SchemaContext (more below)

## Examples

### [Hello World](tests/examples/a_hello_world.py) 

This demonstrates generating a validator for a dataclass.

### [Validated Dataclass](tests/examples/b_validated_dataclass.py) 

This demonstrates generating a validated dataclass

### [Validated Fields](tests/examples/c_field_validations.py)

This demonstrates adding custom validation rules to dataclass fields

### [Custom Class Validations](tests/examples/d_custom_validations.py)

This demonstrates adding fully custom marshalling and validations for a class

### [Beginning with a JSON Schema](tests/examples/e_from_json.py)

This demonstrates starting with a json schema and generating python dataclasses from it.

### Configuring the Context itself

Schemey uses a strategy very similar to marshy for configuration.

Schemey looks for top level modules starting with the name `schemey_config_*`,
sorts them by `priority`, and applies them to the default context by invoking their
`configure` function. [schemey_config_default/__init__.py](schemey_config_default/__init__.py)
contains the default set of factories. 

For example, for a project named `no_more_uuids`, I may add a file `schemey_config_no_more_uuids/__init__.py`:

```
priority = 120  # Applied after default

def configure(context):
    # For some reason, I don't want to be able to generate schemas for uuids!
    context.factories = [
        f for f in context.factories 
        if 'uuid' not in f.__class__.__name__.lower()
    ]

```

## Building The Project

You need an account on pypi before this will work:

```
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install twine
python -m twine upload dist/*
```