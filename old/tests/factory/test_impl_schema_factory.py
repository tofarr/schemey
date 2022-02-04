from dataclasses import dataclass
from unittest import TestCase

from marshy import new_default_context
from marshy.factory import impl_marshaller_factory

from schemey import AnyOfSchema
from schemey import register_impl, register_marshy_impls
from schemey import new_default_schema_context, SchemaContext, get_default_schema_context


@dataclass
class Pet:
    name: str


class Cat(Pet):
    pass


class Dog(Pet):
    pass


class TestImplSchemaFactory(TestCase):

    def test_schema(self):
        context = new_default_schema_context()
        register_impl(Pet, Cat, context)
        register_impl(Pet, Dog, context)
        self._check_pet_schema(context)

    def test_register_marshy_impls(self):
        # Typically this would be done in a marshy config somewhere
        marshy_context = new_default_context()
        impl_marshaller_factory.register_impl(Pet, Cat, marshy_context)
        impl_marshaller_factory.register_impl(Pet, Dog, marshy_context)

        context = new_default_schema_context()
        register_marshy_impls(context, marshy_context)
        self._check_pet_schema(context)

    def test_register_marshy_default(self):
        # Typically this would be done in a marshy config somewhere
        impl_marshaller_factory.register_impl(Pet, Cat)
        impl_marshaller_factory.register_impl(Pet, Dog)

        context = new_default_schema_context()
        register_marshy_impls(context)
        self._check_pet_schema(context)

    def test_register_impl_default(self):
        register_impl(Pet, Cat)
        register_impl(Pet, Dog)
        self._check_pet_schema(get_default_schema_context())

    @staticmethod
    def _check_pet_schema(context: SchemaContext):
        schema = context.create_schema(Pet)
        schemas = [
            context.create_schema(Cat),
            context.create_schema(Dog),
        ]
        expected_schemas = list(sorted(schemas, key=lambda s: s.name))
        assert schemas == expected_schemas
        expected = AnyOfSchema(
            schemas=schema.schemas,
            name='Pet'
        )
        assert schema == expected
