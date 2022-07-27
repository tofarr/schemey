"""
This exists to test annotations support
"""
from __future__ import annotations
from dataclasses import field, dataclass, fields, is_dataclass, MISSING
from typing import Optional, List, Set, get_type_hints
from unittest import TestCase
from uuid import uuid4, UUID

from marshy import dump, load

from schemey.array_schema import ArraySchema
from schemey.boolean_schema import BooleanSchema
from schemey.deferred_schema import DeferredSchema
from schemey.integer_schema import IntegerSchema
from schemey.obj_schema import ObjSchema
from schemey.param_schema import ParamSchema
from schemey.schema_abc import SchemaABC
from schemey.object_schema import ObjectSchema
from schemey.optional_schema import OptionalSchema
from schemey.schema_error import SchemaError
from schemey.schema_context import get_default_schema_context, schema_for_type
from schemey.string_format import StringFormat
from schemey.string_schema import StringSchema


@dataclass
class FutureTag:  # Simple test
    id: int
    title: str = field(metadata=dict(schemey=StringSchema(max_length=255)))
    active: bool = False


@dataclass
class FutureContent:  # Tests dataclasses referencing others
    text: str
    id: UUID = field(default_factory=uuid4())
    title: Optional[str] = None
    tags: Set[FutureTag] = field(default_factory=set)


@dataclass
class FutureNode:  # Mainly tests self referential dataclasses
    title: str
    children: List[FutureNode] = field(default_factory=list)


class TestDataclassFuturesSchema(TestCase):
    def test_generate_schema_for_tag(self):
        context = get_default_schema_context()
        schema = context.get_schema(FutureTag)
        expected = ObjectSchema(
            name="FutureTag",
            required={"id", "title"},
            properties=dict(
                id=IntegerSchema(),
                title=StringSchema(max_length=255),
                active=OptionalSchema(BooleanSchema(), False),
            ),
        )
        self.assertEqual(expected, schema)

    def test_load_and_dump_tag(self):
        self._check_load_and_dump(
            FutureTag,
            dict(
                name="FutureTag",
                type="object",
                additionalProperties=False,
                required=["id", "title"],
                properties=dict(
                    id=dict(type="integer"),
                    title=dict(type="string", maxLength=255),
                    active=dict(type="boolean", default=False),
                ),
            ),
        )

    def test_validate_tag_wrong_type(self):
        schema = schema_for_type(FutureTag)
        json_schema = schema.json_schema
        self.assertEqual(
            [SchemaError("", "type", "not a tag!")],
            list(json_schema.get_schema_errors("not a tag!")),
        )
        self.assertEqual(FutureTag, schema.item_type)

    def test_tag_normalized_type(self):
        standard_type = schema_for_type(FutureTag).json_schema.get_normalized_type(
            {}, dataclass
        )
        self.assertTrue(is_dataclass(standard_type))
        self.assertEqual("FutureTag", standard_type.__name__)
        # noinspection PyDataclass
        attributes = {f.name: (f.type, f.default) for f in fields(standard_type)}
        types = get_type_hints(standard_type, globalns=None, localns=None)
        expected = {f.name: (types[f.name], f.default) for f in fields(FutureTag)}
        self.assertEqual(expected, attributes)

    def test_tag_get_params_schema(self):
        schema = schema_for_type(FutureTag)
        param_schemas = schema.get_param_schemas("")
        expected = [
            ParamSchema("id", IntegerSchema()),
            ParamSchema("title", StringSchema(max_length=255)),
            ParamSchema("active", BooleanSchema(), required=False),
        ]
        self.assertEqual(expected, param_schemas)

    def test_tag_url_params(self):
        schema = schema_for_type(FutureTag)
        tag = FutureTag(1, "A Tag", True)
        url_params = list(schema.to_url_params(tag))
        self.assertEqual([("id", "1"), ("title", "A Tag"), ("active", "1")], url_params)
        loaded = schema.from_url_params(
            {"id": ["1"], "title": ["A Tag"], "active": ["1"]}
        )
        self.assertEqual(tag, loaded)

    def test_tag_url_params_missing_optional(self):
        schema = schema_for_type(FutureTag)
        expected = FutureTag(1, "A Tag")
        loaded = schema.from_url_params({"id": ["1"], "title": ["A Tag"]})
        self.assertEqual(expected, loaded)

    def test_tag_url_params_missing_required(self):
        schema = schema_for_type(FutureTag)
        with self.assertRaises(ValueError):
            schema.from_url_params({"id": ["1"], "active": ["1"]})

    def test_tag_url_params_missing_all_optional(self):
        context = get_default_schema_context()
        schema = ObjSchema(
            json_schema=OptionalSchema(context.get_schema(FutureTag)),
            marshaller=get_default_schema_context().marshaller_context.get_marshaller(
                Optional[FutureTag]
            ),
        )
        self.assertIsNone(schema.from_url_params({}))

    def test_generate_schema_for_content(self):
        context = get_default_schema_context()
        schema = context.get_schema(FutureContent)
        expected = ObjectSchema(
            name="FutureContent",
            required={"text"},
            properties=dict(
                text=StringSchema(),
                id=OptionalSchema(StringSchema(format=StringFormat.UUID)),
                title=OptionalSchema(StringSchema(), None),
                tags=OptionalSchema(
                    ArraySchema(item_schema=context.get_schema(FutureTag), uniqueness=True)
                ),
            ),
        )
        self.assertEqual(expected, schema)

    def test_load_and_dump_content(self):
        self._check_load_and_dump(
            FutureContent,
            {
                "additionalProperties": False,
                "name": "FutureContent",
                "properties": {
                    "id": {"format": "uuid", "type": "string"},
                    "tags": {
                        "items": {
                            "additionalProperties": False,
                            "name": "FutureTag",
                            "properties": {
                                "active": {"default": False, "type": "boolean"},
                                "id": {"type": "integer"},
                                "title": {"maxLength": 255, "type": "string"},
                            },
                            "required": ["id", "title"],
                            "type": "object",
                        },
                        "type": "array",
                        "uniqueness": True,
                    },
                    "text": {"type": "string"},
                    "title": {"type": "string", "default": None},
                },
                "required": ["text"],
                "type": "object",
            },
        )

    def test_content_normalized_type(self):
        existing_types = {}
        standard_type = schema_for_type(FutureContent).json_schema.get_normalized_type(
            existing_types, dataclass
        )
        self.assertTrue(is_dataclass(standard_type))
        self.assertEqual("FutureContent", standard_type.__name__)
        # noinspection PyDataclass
        attributes = {f.name: (f.type, f.default) for f in fields(standard_type)}
        expected = {
            "text": (str, MISSING),
            "id": (Optional[UUID], None),
            "title": (Optional[str], None),
            "tags": (Optional[Set[existing_types.get("FutureTag")]], None),
        }
        self.assertEqual(expected, attributes)

    def test_content_url_params(self):
        schema = schema_for_type(FutureContent)
        self.assertIsNone(schema.json_schema.get_param_schemas(""))

    def test_generate_schema_for_node(self):
        context = get_default_schema_context()
        schema = context.get_schema(FutureNode)
        expected = DeferredSchema(ref="FutureNode", num_usages=2)
        expected.schema = ObjectSchema(
            name="FutureNode",
            required={"title"},
            properties=dict(
                title=StringSchema(),
                children=OptionalSchema(ArraySchema(item_schema=expected)),
            ),
        )
        self.assertEqual(expected, schema)

    def test_load_and_dump_node(self):
        self._check_load_and_dump(
            FutureNode,
            {
                "$ref": "#$defs/FutureNode",
                "$defs": {
                    "FutureNode": {
                        "name": "FutureNode",
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["title"],
                        "properties": {
                            "title": {"type": "string"},
                            "children": {
                                "type": "array",
                                "items": {"$ref": "#$defs/FutureNode"},
                            },
                        },
                    }
                },
            },
        )

    def test_validate_node(self):
        schema = schema_for_type(FutureNode)
        self.assertEqual(
            [], list(schema.get_schema_errors(FutureNode("a", [FutureNode("b"), FutureNode("c")])))
        )
        json_schema = schema.json_schema
        self.assertEqual(
            [SchemaError("", "additional_properties", "invalid_attr")],
            list(json_schema.get_schema_errors(dict(title="foo", invalid_attr="bar"))),
        )
        self.assertEqual(
            [SchemaError("", "missing_properties", "title")],
            list(json_schema.get_schema_errors(dict())),
        )

    def test_node_normalized_type(self):
        existing_types = {}
        standard_type = schema_for_type(FutureNode).json_schema.get_normalized_type(
            existing_types, dataclass
        )
        self.assertTrue(is_dataclass(standard_type))
        self.assertEqual("FutureNode", standard_type.__name__)
        # noinspection PyDataclass
        attributes = {f.name: (f.type, f.default) for f in fields(standard_type)}
        expected = {
            "title": (str, MISSING),
            "children": (Optional[List[existing_types.get("FutureNode")]], None),
        }
        self.assertEqual(expected, attributes)

    def _check_load_and_dump(self, type_, expected_dump):
        context = get_default_schema_context()
        schema = context.get_schema(type_)
        dumped = dump(schema)
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)
