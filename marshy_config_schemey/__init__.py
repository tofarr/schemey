from marshy.marshaller_context import MarshallerContext

from schemey.schema_marshaller import SchemaMarshaller

priority = 100


def configure(context: MarshallerContext):
    context.register_marshaller(SchemaMarshaller())
