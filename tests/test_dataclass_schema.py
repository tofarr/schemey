from dataclasses import field, dataclass
from datetime import datetime
from random import randint
from typing import Optional, List, Set
from unittest import TestCase
from uuid import uuid4, UUID

from marshy.types import ExternalItemType

from schemey.any_of_schema import optional_schema
from schemey.array_schema import ArraySchema
from schemey.boolean_schema import BooleanSchema
from schemey.integer_schema import IntegerSchema
from schemey.json_schema_abc import NoDefault
from schemey.object_schema import ObjectSchema
from schemey.ref_schema import RefSchema
from schemey.schema import Schema
from schemey.schema_error import SchemaError
from schemey.schemey_context import get_default_schemey_context
from schemey.string_format import StringFormat
from schemey.string_schema import StringSchema

_Node = f"{__name__}.Node"

@dataclass
class Tag:
    id: int
    title: str = field(metadata=dict(schemey=StringSchema(max_length=255)))
    active: bool = False


@dataclass
class Content:
    text: str
    id: UUID = field(default_factory=uuid4())
    title: Optional[str] = None
    tags: Set[Tag] = field(default_factory=set)


@dataclass
class Node:
    title: str
    children: List[_Node] = field(default_factory=list)


class TestDataclassSchema(TestCase):

    def test_generate_schema_for_tag(self):
        context = get_default_schemey_context()
        schema = context.get_schema(Tag)
        expected = Schema(
            ObjectSchema(name='Tag', required=['id', 'title'], properties=dict(
                id=IntegerSchema(),
                title=StringSchema(max_length=255),
                active=BooleanSchema(default_value=False)
            )),
            context.marshaller_context.get_marshaller(Tag)
        )
        self.assertEqual(expected, schema)

    def test_generate_schema_for_content(self):
        context = get_default_schemey_context()
        schema = context.get_schema(Content)
        expected = Schema(
            ObjectSchema(name='Content', required=['text'], properties=dict(
                text=StringSchema(),
                id=StringSchema(format=StringFormat.UUID),
                title=optional_schema(StringSchema(), None),
                tags=ArraySchema(item_schema=context.get_schema(Tag).json_schema, uniqueness=True),
            )),
            context.marshaller_context.get_marshaller(Content)
        )
        self.assertEqual(expected, schema)

    def test_generate_schema_for_node(self):
        context = get_default_schemey_context()
        schema = context.get_schema(Node)
        ref_schema = RefSchema()
        expected = Schema(
            ObjectSchema(name='Node', required=['title'], properties=dict(
                title=StringSchema(),
                children=ArraySchema(item_schema=ref_schema),
            )),
            context.marshaller_context.get_marshaller(Node)
        )
        ref_schema.schema = expected.json_schema
        self.assertEqual(expected, schema)
