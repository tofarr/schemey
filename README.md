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

### [Custom JSON Schema Validations](tests/examples/e_custom_json_schema_validations.py)

This demonstrates creating custom json schema validations for things not natively supported by json schema. For 
example, [checking a date against the current time](schemey/json_schema/timestamp.py), or that 
[a property of an object is less than another property of that object](schemey/json_schema/ranges.py).

### [Beginning with a JSON Schema](tests/examples/f_from_json.py)

This demonstrates starting with a json schema and generating python dataclasses from it.

### Configuring the Context itself

Schemey uses [Injecty](https://github.org/tofarr/injecty) for configuration.
The default configuration is [here](injecty_config_schemey/__init__.py)

For example, for a project named `no_more_uuids`, I may add a file `injecty_config_no_more_uuids/__init__.py`:

```
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.factory.uuid_factory import UuidFactory

priority = 120  # Applied after default


def configure(context):
    context.deregister_impl(SchemaFactoryABC, UuidFactory)

```

## Installing local development dependencies

```
python setup.py install easy_install "schemey[dev]"
```

## Release Procedure

![status](https://github.com/tofarr/schemey/actions/workflows/quality.yml/badge.svg?branch=main)

The typical process here is:
* Create a PR with changes. Merge these to main (The `Quality` workflows make sure that your PR
  meets the styling, linting, and code coverage standards).
* New releases created in github are automatically uploaded to pypi
