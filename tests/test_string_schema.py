from datetime import datetime
from unittest import TestCase
from uuid import uuid4, UUID

from marshy import dump, load
from marshy.types import ExternalItemType

from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError
from schemey.schemey_context import get_default_schemey_context
from schemey.string_format import StringFormat
from schemey.string_schema import StringSchema


class TestIntegerSchema(TestCase):

    def test_factory(self):
        context = get_default_schemey_context()
        schema = context.get_schema(str)
        expected = StringSchema()
        self.assertEqual(expected, schema)

    def test_schema_max_length(self):
        schema = StringSchema(max_length=3)
        assert list(schema.get_schema_errors('12')) == []
        assert list(schema.get_schema_errors('123')) == []
        assert list(schema.get_schema_errors('1234')) == [SchemaError('', 'max_length', '1234')]
        errors = list(schema.get_schema_errors('1234', ['foo', 'bar']))
        assert errors == [SchemaError('foo/bar', 'max_length', '1234')]
        self._check_dump_and_load(schema, dict(type='string', maxLength=3))

    def test_schema_min_length(self):
        schema = StringSchema(min_length=3)
        assert list(schema.get_schema_errors('1234')) == []
        assert list(schema.get_schema_errors('123')) == []
        assert list(schema.get_schema_errors('12')) == [SchemaError('', 'min_length', '12')]
        assert list(schema.get_schema_errors('12', ['foo', 'bar'])) == [SchemaError('foo/bar', 'min_length', '12')]
        self._check_dump_and_load(schema, dict(type='string', minLength=3))

    def test_schema_pattern(self):
        schema = StringSchema(pattern='[a-z]+$')
        assert list(schema.get_schema_errors("ab")) == []
        assert list(schema.get_schema_errors("a1")) == [SchemaError('', 'pattern', 'a1')]
        self._check_dump_and_load(schema, dict(type='string', pattern='[a-z]+$'))

    def test_format_date(self):
        schema = StringSchema(format=StringFormat.DATE)
        assert list(schema.get_schema_errors("2021-11-01")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:date', 'foobar')]
        assert list(schema.get_schema_errors("2021-13-01")) == [SchemaError('', 'format:date', '2021-13-01')]
        errors = list(schema.get_schema_errors("2021-12-01T01:02:03"))
        assert errors == [SchemaError('', 'format:date', '2021-12-01T01:02:03')]
        self._check_dump_and_load(schema, dict(type='string', format='date'))

    def test_format_date_time(self):
        schema = StringSchema(format=StringFormat.DATE_TIME)
        assert list(schema.get_schema_errors("2021-11-01T13:04:01")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:date-time', 'foobar')]
        self._check_dump_and_load(schema, dict(type='string', format='date-time'))

    def test_datetime(self):
        context = get_default_schemey_context()
        schema = context.get_schema(datetime)
        self._check_dump_and_load(schema, dict(type='string', format='date-time'))

    def test_format_time(self):
        schema = StringSchema(format=StringFormat.TIME)
        assert list(schema.get_schema_errors("23:15:00")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:time', 'foobar')]
        self._check_dump_and_load(schema, dict(type='string', format='time'))

    def test_format_email(self):
        schema = StringSchema(format=StringFormat.EMAIL)
        assert list(schema.get_schema_errors("foo@bar.com")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:email', 'foobar')]
        self._check_dump_and_load(schema, dict(type='string', format='email'))

    def test_format_hostname(self):
        schema = StringSchema(format=StringFormat.HOSTNAME)
        assert list(schema.get_schema_errors("chicken.sandwich")) == []
        errors = list(schema.get_schema_errors("chicken sandwich"))
        assert errors == [SchemaError('', 'format:hostname', 'chicken sandwich')]
        self._check_dump_and_load(schema, dict(type='string', format='hostname'))

    def test_format_ipv4(self):
        schema = StringSchema(format=StringFormat.IPV4)
        assert list(schema.get_schema_errors("192.168.1.1")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:ipv4', 'foobar')]
        self._check_dump_and_load(schema, dict(type='string', format='ipv4'))

    def test_format_ipv6(self):
        schema = StringSchema(format=StringFormat.IPV6)
        assert list(schema.get_schema_errors('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:ipv6', 'foobar')]
        self._check_dump_and_load(schema, dict(type='string', format='ipv6'))

    def test_format_uuid(self):
        schema = StringSchema(format=StringFormat.UUID)
        assert list(schema.get_schema_errors(str(uuid4()))) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:uuid', 'foobar')]
        self._check_dump_and_load(schema, dict(type='string', format='uuid'))

    def test_uuid(self):
        context = get_default_schemey_context()
        schema = context.get_schema(UUID)
        self._check_dump_and_load(schema, dict(type='string', format='uuid'))

    def test_format_uri(self):
        schema = StringSchema(format=StringFormat.URI)
        assert list(schema.get_schema_errors("https://foo.com/bar?zap=bang")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:uri', 'foobar')]
        self._check_dump_and_load(schema, dict(type='string', format='uri'))

    def test_schema_wrong_type(self):
        schema = StringSchema()
        self.assertEqual([SchemaError('', 'type', 10)], list(schema.get_schema_errors(10)))

    def _check_dump_and_load(self, schema: StringSchema, expected: ExternalItemType):
        dumped = dump(schema)
        self.assertEqual(expected, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(loaded, schema)
