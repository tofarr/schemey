from unittest import TestCase

from jsonschema import ValidationError

from schemey import schema_from_json


def _range_schema(allow_equal: bool):
    return schema_from_json({
        "name": "RangeTest",
        "type": "object",
        "properties": {
            "min_value": {"type": "integer", "minimum": 5},
            "max_value": {"type": "integer"}
        },
        "additionalProperties": False,
        "required": ["min_value", "max_value"],
        "ranges": [{
            "minProperty": "min_value",
            "maxProperty": "max_value",
            "allowEqual": allow_equal
        }]
    })


class TestRanges(TestCase):

    def test_ranges(self):
        schema = _range_schema(False)
        schema.validate(dict(min_value=5, max_value=7))
        with self.assertRaises(ValidationError):
            schema.validate(dict(min_value=13, max_value=11))
        with self.assertRaises(ValidationError):
            schema.validate(dict(min_value=17, max_value=17))

    def test_ranges_allow_equal(self):
        schema = _range_schema(True)
        schema.validate(dict(min_value=5, max_value=7))
        with self.assertRaises(ValidationError):
            schema.validate(dict(min_value=13, max_value=11))
        schema.validate(dict(min_value=17, max_value=17))
        list(schema.iter_errors([]))
