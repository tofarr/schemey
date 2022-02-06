from dataclasses import field, dataclass
from datetime import datetime
from typing import Optional, List, Set, Tuple
from unittest import TestCase
from uuid import uuid4, UUID

from marshy import dump, load

from schemey.array_schema import ArraySchema
from schemey.boolean_schema import BooleanSchema
from schemey.deferred_schema import DeferredSchema
from schemey.integer_schema import IntegerSchema
from schemey.schema_abc import SchemaABC
from schemey.object_schema import ObjectSchema
from schemey.optional_schema import OptionalSchema
from schemey.schema_error import SchemaError
from schemey.schema_context import get_default_schema_context, schema_for_type
from schemey.string_format import StringFormat
from schemey.string_schema import StringSchema

_Node = f"{__name__}.Node"
_Immutable = f"{__name__}.Immutable"


@dataclass
class Tag:  # Simple test
    id: int
    title: str = field(metadata=dict(schemey=StringSchema(max_length=255)))
    active: bool = False


@dataclass
class Content:  # Tests dataclasses referencing others
    text: str
    id: UUID = field(default_factory=uuid4())
    title: Optional[str] = None
    tags: Set[Tag] = field(default_factory=set)


@dataclass
class Node:  # Mainly tests self referential dataclasses
    title: str
    children: List[_Node] = field(default_factory=list)


@dataclass(frozen=True)
class ImmutableLabel:  # Tests immutability and having no required properties
    title: str = "Label"
    updated_at: datetime = field(default_factory=datetime.now)


DEFAULT_PRIMARY_LABEL = ImmutableLabel('Primary')
DEFAULT_SECONDARY_LABEL = (ImmutableLabel('Secondary'),)


@dataclass(frozen=True)
class ImmutableWidget:
    label: ImmutableLabel = DEFAULT_PRIMARY_LABEL
    secondary_labels: Tuple[ImmutableLabel, ...] = DEFAULT_SECONDARY_LABEL


class TestDataclassSchema(TestCase):

    def test_generate_schema_for_tag(self):
        context = get_default_schema_context()
        schema = context.get_schema(Tag)
        expected = ObjectSchema(name='Tag', required={'id', 'title'}, properties=dict(
            id=IntegerSchema(),
            title=StringSchema(max_length=255),
            active=OptionalSchema(BooleanSchema(), False)
        ))
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

    def test_validate_tag_wrong_type(self):
        schema = schema_for_type(Tag)
        json_schema = schema.json_schema
        self.assertEqual([SchemaError('', 'type', 'not a tag!')], list(json_schema.get_schema_errors('not a tag!')))
        self.assertEqual(Tag, schema.item_type)

    def test_generate_schema_for_content(self):
        context = get_default_schema_context()
        schema = context.get_schema(Content)
        expected = ObjectSchema(name='Content', required={'text'}, properties=dict(
            text=StringSchema(),
            id=OptionalSchema(StringSchema(format=StringFormat.UUID)),
            title=OptionalSchema(StringSchema(), None),
            tags=OptionalSchema(ArraySchema(item_schema=context.get_schema(Tag), uniqueness=True))
        ))
        self.assertEqual(expected, schema)

    def test_load_and_dump_content(self):
        self._check_load_and_dump(Content, {
            'additionalProperties': False,
            'name': 'Content',
            'properties': {
                'id': {'format': 'uuid', 'type': 'string'},
                'tags': {
                    'items': {
                        'additionalProperties': False,
                        'name': 'Tag',
                        'properties': {
                            'active': {'default': False, 'type': 'boolean'},
                            'id': {'type': 'integer'},
                            'title': {'maxLength': 255, 'type': 'string'}
                        },
                        'required': ['id', 'title'],
                        'type': 'object'
                    },
                    'type': 'array',
                    'uniqueness': True
                },
                'text': {'type': 'string'},
                'title': {'type': 'string', 'default': None}
            },
            'required': ['text'],
            'type': 'object'
        })

    def test_generate_schema_for_node(self):
        context = get_default_schema_context()
        schema = context.get_schema(Node)
        expected = DeferredSchema(ref='Node', num_usages=2)
        expected.schema = ObjectSchema(name='Node', required={'title'}, properties=dict(
            title=StringSchema(),
            children=OptionalSchema(ArraySchema(item_schema=expected))
        ))
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

    def test_validate_node(self):
        schema = schema_for_type(Node)
        self.assertEqual([], list(schema.get_schema_errors(Node('a', [Node('b'), Node('c')]))))
        json_schema = schema.json_schema
        self.assertEqual([SchemaError('', 'additional_properties', 'invalid_attr')],
                         list(json_schema.get_schema_errors(dict(title='foo', invalid_attr='bar'))))
        self.assertEqual([SchemaError('', 'missing_properties', 'title')],
                         list(json_schema.get_schema_errors(dict())))

    def test_generate_schema_for_immutable_label(self):
        context = get_default_schema_context()
        schema = context.get_schema(ImmutableLabel)
        expected = ObjectSchema(
            properties={
                'title': OptionalSchema(
                    schema=StringSchema(min_length=None, max_length=None, pattern=None, format=None),
                    default='Label'
                ),
                'updated_at': OptionalSchema(
                    StringSchema(min_length=None, max_length=None, pattern=None, format=StringFormat.DATE_TIME)
                )
            },
            name='ImmutableLabel'
        )
        self.assertEqual(expected, schema)

    def test_load_and_dump_immutable_label(self):
        self._check_load_and_dump(ImmutableLabel, {
            'name': 'ImmutableLabel',
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'title': {'type': 'string', 'default': 'Label'},
                'updated_at': {'type': 'string', 'format': 'date-time'}
            }
        })

    def test_generate_schema_for_immutable_widget(self):
        context = get_default_schema_context()
        schema = context.get_schema(ImmutableWidget)
        label_schema = context.get_schema(ImmutableLabel)
        expected = ObjectSchema(
            properties={
                'label': OptionalSchema(context.get_schema(ImmutableLabel), dump(DEFAULT_PRIMARY_LABEL)),
                'secondary_labels': OptionalSchema(
                    schema=ArraySchema(item_schema=label_schema),
                    default=dump(DEFAULT_SECONDARY_LABEL, Tuple[ImmutableLabel, ...])
                )
            },
            name='ImmutableWidget'
        )
        self.assertEqual(expected, schema)

    def test_load_and_dump_immutable_widget(self):
        self._check_load_and_dump(ImmutableWidget, {
            'additionalProperties': False,
            'name': 'ImmutableWidget',
            'properties': {
                'label': {
                    'additionalProperties': False,
                    'default': {
                        'title': 'Primary',
                        'updated_at': DEFAULT_PRIMARY_LABEL.updated_at.isoformat()
                    },
                    'name': 'ImmutableLabel',
                    'properties': {
                        'title': {
                            'default': 'Label',
                            'type': 'string'
                        },
                        'updated_at': {
                            'format': 'date-time',
                            'type': 'string'
                        }
                    },
                    'type': 'object'
                },
                'secondary_labels': {
                    'default': [
                        {
                            'title': 'Secondary',
                            'updated_at': DEFAULT_SECONDARY_LABEL[0].updated_at.isoformat()
                        }
                    ],
                    'items': {
                        'additionalProperties': False,
                        'name': 'ImmutableLabel',
                        'properties': {
                            'title': {
                                'default': 'Label',
                                'type': 'string'
                            },
                            'updated_at': {
                                'format': 'date-time',
                                'type': 'string'
                            }
                        },
                        'type': 'object'
                    },
                    'type': 'array'
                }
            },
            'type': 'object'
        })

    def _check_load_and_dump(self, type_, expected_dump):
        context = get_default_schema_context()
        schema = context.get_schema(type_)
        dumped = dump(schema)
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)
