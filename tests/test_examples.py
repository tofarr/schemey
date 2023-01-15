from unittest import TestCase


class TestExamples(TestCase):
    def test_a(self):
        from tests.examples import a_hello_world

        assert a_hello_world.errors

    def test_b(self):
        from tests.examples import b_validated_dataclass

        assert b_validated_dataclass.greeter

    def test_c(self):
        from tests.examples import c_field_validations

        assert c_field_validations.validator

    def test_d(self):
        from tests.examples import d_custom_validations

        assert d_custom_validations.validator

    def test_e(self):
        from tests.examples import e_custom_json_schema_validations

        assert e_custom_json_schema_validations.errors

    def test_f(self):
        from tests.examples import f_from_json

        assert f_from_json.User
