from unittest import TestCase


class TestExamples(TestCase):

    def test_a(self):
        from tests.examples import a_hello_world
        assert a_hello_world.errors

    def test_b(self):
        from tests.examples import b_json_conversion
        assert b_json_conversion.schema_json

    def test_c(self):
        from tests.examples import c_self_references
        assert c_self_references.schema_json

    def test_d(self):
        from tests.examples import d_custom_field_schema
        assert d_custom_field_schema.errors
