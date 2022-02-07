from marshy.marshaller_context import MarshallerContext

from schemey.factory.schema_marshaller_factory import SchemaMarshallerFactory

priority = 100


def configure(context: MarshallerContext):
    context.register_factory(SchemaMarshallerFactory())
