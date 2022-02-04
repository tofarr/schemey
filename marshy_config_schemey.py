from marshy.marshaller_context import MarshallerContext

from schemey.factory.json_schema_marshaller_factory import JsonSchemaMarshallerFactory

priority = 100


def configure(context: MarshallerContext):
    context.register_factory(JsonSchemaMarshallerFactory())
