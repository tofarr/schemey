from abc import abstractmethod, ABC
from typing import Iterator, Optional, List, Generic, TypeVar

from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller_context import MarshallerContext
from marshy.types import ExternalType

from persisty.schema.schema_error import SchemaError

T = TypeVar('T')


class SchemaABC(ABC, Generic[T]):
    """
    A Schema for a particular type of object, which may be marshalled into a JsonSchema. Json Schemas are fundamentally
    extensible and tolerant of additional unknown attributes. We use this to pass additonal data to clients and store
    things that may not be part of the general spec.
    """

    @abstractmethod
    def get_schema_errors(self,
                          item: T,
                          current_path: Optional[List[str]] = None
                          ) -> Iterator[SchemaError]:
        """ Get the validation errors for the item given. """

    @staticmethod
    def __marshaller_factory__(cls, marshaller_context: MarshallerContext):
        """
        Get the marshaller for schemas. Custom marshallers can override this
        """
        from persisty.schema.marshaller.array_schema_marshaller import ArraySchemaMarshaller
        from persisty.schema.marshaller.boolean_schema_marshaller import BooleanSchemaMarshaller
        from persisty.schema.marshaller.number_schema_marshaller import NumberSchemaMarshaller
        from persisty.schema.marshaller.string_schema_marshaller import StringSchemaMarshaller
        from persisty.schema.marshaller.object_schema_marshaller import ObjectSchemaMarshaller
        from persisty.schema.marshaller.null_schema_marshaller import NullSchemaMarshaller
        from persisty.schema.marshaller.schema_marshaller import SchemaMarshaller
        deferred = DeferredMarshaller(SchemaABC, marshaller_context)
        marshallers_by_name = {
            'array': ArraySchemaMarshaller(deferred),
            'boolean': BooleanSchemaMarshaller(),
            'integer': NumberSchemaMarshaller(),
            'number': NumberSchemaMarshaller(),
            'string': StringSchemaMarshaller(),
            'object': ObjectSchemaMarshaller(deferred),
            None: NullSchemaMarshaller(),
        }
        return SchemaMarshaller(marshallers_by_name)
