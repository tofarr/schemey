from abc import abstractmethod, ABC
from typing import Iterator, Optional, List, Generic, TypeVar, Type, Dict

from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller_context import MarshallerContext

from schema.schema_error import SchemaError

T = TypeVar('T')
_SchemaABC = f'{__name__}.SchemaABC'


class SchemaABC(ABC, Generic[T]):
    """
    A Schema for a particular type of object, which may be marshalled into a JsonSchema. Json Schemas are fundamentally
    extensible and tolerant of additional unknown attributes. We use this to pass additonal data to clients and store
    things that may not be part of the general spec.
    """

    @abstractmethod
    def get_schema_errors(self,
                          item: T,
                          defs: Optional[Dict[str, _SchemaABC]],
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        """ Get the validation errors for the item given. """

    @staticmethod
    def __marshaller_factory__(cls, marshaller_context: MarshallerContext):
        """
        Get the marshaller for schemas. Custom marshallers can override this
        """
        from schema.marshaller.array_schema_marshaller import ArraySchemaMarshaller
        from schema.marshaller.boolean_schema_marshaller import BooleanSchemaMarshaller
        from schema.marshaller.number_schema_marshaller import NumberSchemaMarshaller
        from schema.marshaller.string_schema_marshaller import StringSchemaMarshaller
        from schema.marshaller.object_schema_marshaller import ObjectSchemaMarshaller
        from schema.marshaller.null_schema_marshaller import NullSchemaMarshaller
        from schema.marshaller.schema_marshaller import SchemaMarshaller
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
