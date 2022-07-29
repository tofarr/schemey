from dataclasses import field, dataclass, fields
from datetime import datetime
from typing import Optional, List
from unittest import TestCase
from uuid import uuid4, UUID

from jsonschema import ValidationError
from marshy import dump, load

from schemey import schema_from_type, schema_from_json
from schemey.schema import str_schema, Schema

_Node = f"{__name__}.Node"
_Immutable = f"{__name__}.Immutable"


@dataclass
class Tag:  # Simple test
    id: int
    title: str = field(metadata=dict(schemey=str_schema(max_length=255)))
    active: bool = False


@dataclass
class Content:  # Tests dataclasses referencing others
    """A content object"""

    text: str
    id: UUID = field(default_factory=uuid4)
    title: Optional[str] = None
    tags: List[Tag] = field(default_factory=set)


@dataclass
class Node:  # Mainly tests self referential dataclasses
    """A node object"""

    title: str
    children: List[_Node] = field(default_factory=list)


@dataclass(frozen=True)
class ImmutableLabel:  # Tests immutability and having no required properties
    title: str = "Label"
    updated_at: datetime = field(default_factory=datetime.now)


# noinspection PyPep8Naming
class TestDataclassSchema(TestCase):
    def test_generate_schema_for_tag(self):
        schema = schema_from_type(Tag)
        expected = Schema(
            schema={
                "type": "object",
                "name": "Tag",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string", "maxLength": 255},
                    "active": {"type": "boolean", "default": False},
                },
                "additionalProperties": False,
                "required": ["id", "title"],
                "description": "Tag(id: int, title: str, active: bool = False)",
            },
            python_type=Tag,
        )
        self.assertEqual(expected, schema)

    def test_validate_tag(self):
        schema = schema_from_type(Tag)
        item = dump(Tag(10, "Ten", True))
        schema.validate(item)
        schema.validate({"id": 10, "title": "Ten"})
        with self.assertRaises(ValidationError):
            schema.validate({})
        with self.assertRaises(ValidationError):
            schema.validate({"id": 10, "title": 5})

    def test_generate_schema_for_content(self):
        schema = schema_from_type(Content)
        expected = Schema(
            schema={
                "type": "object",
                "name": "Content",
                "properties": {
                    "text": {"type": "string"},
                    "id": {"type": "string", "format": "uuid"},
                    "title": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "default": None,
                    },
                    "tags": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "name": "Tag",
                            "properties": {
                                "id": {"type": "integer"},
                                "title": {"type": "string", "maxLength": 255},
                                "active": {"type": "boolean", "default": False},
                            },
                            "additionalProperties": False,
                            "required": ["id", "title"],
                            "description": "Tag(id: int, title: str, active: bool = False)",
                        },
                    },
                },
                "additionalProperties": False,
                "required": ["text"],
                "description": "A content object",
            },
            python_type=Content,
        )
        self.assertEqual(expected, schema)

    def test_validate_content(self):
        schema = schema_from_type(Content)
        item = dump(Content(text="Some content", tags=[Tag(1, "Foo"), Tag(2, "Bar")]))
        schema.validate(item)

    def test_generate_schema_for_node(self):
        schema = schema_from_type(Node)
        expected = Schema(
            schema={
                "type": "object",
                "name": "Node",
                "properties": {
                    "title": {"type": "string"},
                    "children": {"type": "array", "items": {"$ref": "#"}},
                },
                "additionalProperties": False,
                "required": ["title"],
                "description": "A node object",
            },
            python_type=Node,
        )
        self.assertEqual(expected, schema)

    # noinspection PyDataclass
    def test_generate_node_from_schema(self):
        expected = schema_from_type(Node)
        schema = schema_from_json(expected.schema)
        # noinspection PyPep8Naming
        Node_ = schema.python_type
        self.assertEqual(["title", "children"], [f.name for f in fields(Node_)])
        self.assertEqual([str, List[Node_]], [f.type for f in fields(Node_)])
        string = str(Node_("Foobar", [Node_("Child", [])]))
        expected_str = (
            "Node(title='Foobar', children=[Node(title='Child', children=[])])"
        )
        self.assertEqual(expected_str, string)

    def test_load_and_dump_node(self):
        schema = schema_from_type(Node)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(schema.schema, loaded.schema)
        self.assertEqual(Node.__doc__.strip(), loaded.python_type.__doc__)
        # noinspection PyDataclass
        self.assertEqual(
            [f.name for f in fields(Node)],
            [f.name for f in fields(loaded.python_type)],
        )

    def test_validate_node(self):
        schema = schema_from_type(Node)
        item = dump(Node("a", [Node("b"), Node("c")]))
        schema.validate(item)

    def test_generate_schema_for_immutable_label(self):
        schema = schema_from_type(ImmutableLabel)
        expected = Schema(
            schema={
                "type": "object",
                "name": "ImmutableLabel",
                "properties": {
                    "title": {"type": "string", "default": "Label"},
                    "updated_at": {"type": "string", "format": "date-time"},
                },
                "additionalProperties": False,
                "required": [],
                "description": "ImmutableLabel(title: str = 'Label', updated_at: datetime.datetime = <factory>)",
            },
            python_type=ImmutableLabel,
        )
        self.assertEqual(expected, schema)

    # noinspection PyDataclass
    def test_generate_immutable_label_from_schema(self):
        expected = schema_from_type(ImmutableLabel)
        schema = schema_from_json(expected.schema)
        ImmutableLabel_ = schema.python_type
        self.assertEqual(
            ["updated_at", "title"], [f.name for f in fields(ImmutableLabel_)]
        )
        self.assertEqual([datetime, str], [f.type for f in fields(ImmutableLabel_)])
        string = str(
            ImmutableLabel_(datetime.fromisoformat("2020-01-01T00:00:00"), "Foobar")
        )
        expected_str = "ImmutableLabel(updated_at=datetime.datetime(2020, 1, 1, 0, 0), title='Foobar')"
        self.assertEqual(expected_str, string)

    def test_resolve_futures(self):
        from schemey.factory.dataclass_schema_factory import _resolve_futures

        # noinspection PyTypeChecker
        self.assertEqual(Node, _resolve_futures("Node", "Node", Node))
