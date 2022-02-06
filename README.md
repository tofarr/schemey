# Schemey - Json Schemas for Python.

This project allows for generation of json schema objects based on python
dataclasses, along with customization of said schemas. Schemas may then
be used to validate object graphs.

The general idea is that the framework should not insist on any particular
data structure or paradigm - it is designed to be extensible, and out of the box support
is provided for iterable types, dataclasses, enums, timestamps and primitives.

Serialization is provided using marshy.

Current test coverage is at 100%

## Why did you build this?

There were undocumented gaps in the functionality of existing solutions
that made using them untenable.

## Installation

`pip install schemey`

## Examples

### [Hello World](tests/examples/a_hello_world.py) 

This demonstrates generating a standard schema for a dataclass.

### [JSON Conversion](tests/examples/b_json_conversion.py) 

This demonstrates dumping a json schema for a dataclass

Deserializing json schemas is currently minimally supported.
(Due to the complexity of extracting references from anywhere in
the document and the evolving nature of the spec). The intended 
workflow is to start with a Python dataclass and then convert to
a json schema rather than the other way around.

### [JSON Conversion](tests/examples/c_self_references.py)

Self referencing data structures are supported out of the box.

### [Adding Custom Schemas for Dataclass Fields](tests/examples/d_custom_field_schema.py)

Add a schema to the `schemey` attribute of a metadata field for a dataclass to specify a custom schema

The following schemas are defined out of the box (Feel free to add your own!):

* [AnyOfSchema](schemey/any_of_schema.py): For polymorphic constraints
* [ArraySchema](schemey/array_schema.py): For arrays
* [BooleanSchema](schemey/boolean_schema.py): For boolean values
* [ConstSchema](schemey/const_schema.py): For constant values
* [DeferredSchema](schemey/deferred_schema.py): Deferred schema - (used for self referential schemas)
* [EnumSchema](schemey/enum_schema.py): For enums
* [IntegerSchema](schemey/integer_schema.py): For integer validation
* [NullSchema](schemey/null_schema.py): For null validation
* [NumberSchema](schemey/number_schema.py): For float validation
* [NullSchema](schemey/null_schema.py): For None / null values
* [ObjectSchema](schemey/object_schema.py): For objects
* [OptionalSchema](schemey/optional_schema.py): For optional values
* [StringSchema](schemey/string_schema.py): For string validation. (Including regex, format and length constraints)
* [TupleSchema](schemey/tuple_schema.py): For tuple validation.

## Architectural Concepts.

* A [Schema](schemey/schema_abc.py) is used to validate instances of a type
* A [Factory](schemey/factory/schema_factory_abc.py) is used to create schemas for python types
* A [Loader](schemey/loader/schema_loader_abc.py) is used to generate schemas from raw json. (An alternative to factories)
* A [Context](schemey/schema_context.py) coordinates the operations between schemas and factories (Using
  the default context leads to a shorter syntax, but less flexibility)

## Specifying a Schema for a Class

Below we outline the process of completely customizing schema generation and marshalling.
The simplest way to specify a schema for a class is to define the __schema_factory__ class
property. For example, imagine a situation where a 3D point is defined in javascript
as an array of 3 numbers, [x, y, z].

You write a dataclass to describe this in python, with a custom marshaller (As per the marshy
documentation), but the marshalled schema no longer matches the marshalled dataclass.
You will need to define a custom schema and marshaller for the class too.

* [3D Example - Affects the Global Context](tests/test_factory.py)

### Specify a Schema for a Class by factory

Instead of overriding the __schema_factory__ / __marshaller_factory__
methods, it is possible to register a factory for your schema with
your schema context using the `register_schema` method.

It is also possible to register implementations for abstract classes / duck typing via the 
* [2D Example - Isolated from Other Contexts](tests/test_custom_schema.py)


## Building The Project

You need an account on pypi before this will work:

```
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install twine
python -m twine upload dist/*
```