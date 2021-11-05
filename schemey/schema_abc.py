from abc import abstractmethod, ABC
from typing import Iterator, Optional, List, Generic, TypeVar, Dict

from marshy.marshaller.deferred_marshaller import DeferredMarshaller
from marshy.marshaller_context import MarshallerContext

from schemey.schema_error import SchemaError

T = TypeVar('T')
_SchemaABC = f'{__name__}.SchemaABC'


class SchemaABC(ABC, Generic[T]):
    """
    A Schema for a particular type of object, which may be marshalled into a JsonSchema. Json Schemas are fundamentally
    extensible and tolerant of additional unknown attributes. We use this to pass additional data to clients and store
    things that may not be part of the general spec.
    """

    @abstractmethod
    def get_schema_errors(self,
                          item: T,
                          defs: Optional[Dict[str, _SchemaABC]],
                          current_path: Optional[List[str]] = None,
                          ) -> Iterator[SchemaError]:
        """ Get the validation errors for the item given. """

    def validate(self,
                 item: T,
                 defs: Optional[Dict[str, _SchemaABC]] = None,
                 current_path: Optional[List[str]] = None,
                 ):
        """ Validate the item given """
        if defs is None:
            defs = {}
        errors = self.get_schema_errors(item, defs, current_path)
        error = next(errors, None)
        if error:
            raise error

    # noinspection PyUnusedLocal
    @staticmethod
    def __marshaller_factory__(cls, marshaller_context: MarshallerContext):
        """
        Get the marshaller for schemas. Custom marshallers can override this
        """
        from schemey.marshaller.array_schema_marshaller import ArraySchemaMarshaller
        from schemey.marshaller.boolean_schema_marshaller import BooleanSchemaMarshaller
        from schemey.marshaller.number_schema_marshaller import NumberSchemaMarshaller
        from schemey.marshaller.string_schema_marshaller import StringSchemaMarshaller
        from schemey.marshaller.object_schema_marshaller import ObjectSchemaMarshaller
        from schemey.marshaller.null_schema_marshaller import NullSchemaMarshaller
        from schemey.marshaller.schema_marshaller import SchemaMarshaller
        deferred = DeferredMarshaller(SchemaABC, marshaller_context)
        marshallers_by_name = {
            'array': ArraySchemaMarshaller(deferred),
            'boolean': BooleanSchemaMarshaller(),
            'integer': NumberSchemaMarshaller(),
            'number': NumberSchemaMarshaller(),
            'string': StringSchemaMarshaller(),
            'object': ObjectSchemaMarshaller(deferred),
            'null': NullSchemaMarshaller(),
        }
        return SchemaMarshaller(marshallers_by_name)