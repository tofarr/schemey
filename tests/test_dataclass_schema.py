from dataclasses import field, dataclass
from typing import Optional, List, Set
from unittest import TestCase
from uuid import uuid4, UUID

from marshy import dump, load

from schemey.any_of_schema import optional_schema
from schemey.array_schema import ArraySchema
from schemey.boolean_schema import BooleanSchema
from schemey.deferred_schema import DeferredSchema
from schemey.integer_schema import IntegerSchema
from schemey.json_schema_abc import JsonSchemaABC
from schemey.object_schema import ObjectSchema
from schemey.schema import Schema
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
                active=BooleanSchema(default=False)
            )),
            context.marshaller_context.get_marshaller(Tag)
        )
        self.assertEqual(expected, schema)

    def test_load_and_dump_tag(self):
        self._check_load_and_dump(Tag, dict(
            name='Tag',
            type='object',
            additionalProperties=False,
            required=['id', 'title'],
            properties=dict(
                id=dict(type='integer'),
                title=dict(type='string', maxLength=255),
                active=dict(type='boolean', default=False),
            )
        ))

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

    def test_load_and_dump_content(self):
        self._check_load_and_dump(Content, dict(
            name='Content',
            type='object',
            additionalProperties=False,
            required=['text'],
            properties=dict(
                text=dict(type='string'),
                id=dict(type='string', format='uuid'),
                title=dict(anyOf=[dict(type='null'), dict(type='string')], default=None),
                tags=dict(type='array', uniqueness=True, items=dict(
                    name='Tag',
                    type='object',
                    additionalProperties=False,
                    required=['id', 'title'],
                    properties=dict(
                        id=dict(type='integer'),
                        title=dict(type='string', maxLength=255),
                        active=dict(type='boolean', default=False),
                    )
                )),
            )
        ))

    def test_generate_schema_for_node(self):
        context = get_default_schemey_context()
        schema = context.get_schema(Node)
        expected = DeferredSchema(ref='Node', num_usages=2)
        expected.schema = ObjectSchema(name='Node', required=['title'], properties=dict(
            title=StringSchema(),
            children=ArraySchema(item_schema=expected),
        ))
        expected = Schema(expected, context.marshaller_context.get_marshaller(Node))
        self.assertEqual(expected, schema)

    def test_load_and_dump_node(self):
        self._check_load_and_dump(Node, {
            '$ref': '#$defs/Node',
            '$defs': {
                'Node': {
                    'name': 'Node',
                    'type': 'object',
                    'additionalProperties': False,
                    'required': ['title'],
                    'properties': {
                        'title': {'type': 'string'},
                        'children': {
                            'type': 'array',
                            'items': {
                                '$ref': '#$defs/Node'
                            }
                        }
                    }
                }
            }
        })

    def _check_load_and_dump(self, type_, expected_dump):
        context = get_default_schemey_context()
        schema = context.get_json_schema(type_)
        dumped = dump(schema)
        self.assertEqual(expected_dump, dumped)
        loaded = load(JsonSchemaABC, dumped)
        self.assertEqual(schema, loaded)