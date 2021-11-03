from unittest import TestCase
from uuid import uuid4

from persisty.schema.schema_error import SchemaError
from persisty.schema.string_format import StringFormat
from persisty.schema.string_schema import StringSchema


class TestNumberSchema(TestCase):

    def test_schema_max_length(self):
        schema = StringSchema(max_length=3)
        assert list(schema.get_schema_errors('12')) == []
        assert list(schema.get_schema_errors('123')) == []
        assert list(schema.get_schema_errors('1234')) == [SchemaError('', 'max_length', '1234')]
        assert list(schema.get_schema_errors('1234', ['foo', 'bar'])) == [SchemaError('foo/bar', 'max_length', '1234')]

    def test_schema_min_length(self):
        schema = StringSchema(min_length=3)
        assert list(schema.get_schema_errors('1234')) == []
        assert list(schema.get_schema_errors('123')) == []
        assert list(schema.get_schema_errors('12')) == [SchemaError('', 'min_length', '12')]
        assert list(schema.get_schema_errors('12', ['foo', 'bar'])) == [SchemaError('foo/bar', 'min_length', '12')]

    def test_schema_pattern(self):
        schema = StringSchema(pattern='[a-z]+$')
        assert list(schema.get_schema_errors("ab")) == []
        assert list(schema.get_schema_errors("a1")) == [SchemaError('', 'pattern', 'a1')]

    def test_format_date(self):
        schema = StringSchema(format=StringFormat.DATE)
        assert list(schema.get_schema_errors("2021-11-01")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:date', 'foobar')]
        assert list(schema.get_schema_errors("2021-13-01")) == [SchemaError('', 'format:date', '2021-13-01')]
        errors = list(schema.get_schema_errors("2021-12-01T01:02:03"))
        assert errors == [SchemaError('', 'format:date', '2021-12-01T01:02:03')]

    def test_format_date_time(self):
        schema = StringSchema(format=StringFormat.DATE_TIME)
        assert list(schema.get_schema_errors("2021-11-01T13:04:01")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:date-time', 'foobar')]

    def test_format_time(self):
        schema = StringSchema(format=StringFormat.TIME)
        assert list(schema.get_schema_errors("23:15:00")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:time', 'foobar')]

    def test_format_email(self):
        schema = StringSchema(format=StringFormat.EMAIL)
        assert list(schema.get_schema_errors("foo@bar.com")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:email', 'foobar')]

    def test_format_hostname(self):
        schema = StringSchema(format=StringFormat.HOSTNAME)
        assert list(schema.get_schema_errors("chicken.sandwich")) == []
        errors = list(schema.get_schema_errors("chicken sandwich"))
        assert errors == [SchemaError('', 'format:hostname', 'chicken sandwich')]

    def test_format_ipv4(self):
        schema = StringSchema(format=StringFormat.IPV4)
        assert list(schema.get_schema_errors("192.168.1.1")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:ipv4', 'foobar')]

    def test_format_ipv6(self):
        schema = StringSchema(format=StringFormat.IPV6)
        assert list(schema.get_schema_errors('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:ipv6', 'foobar')]

    def test_format_uuid(self):
        schema = StringSchema(format=StringFormat.UUID)
        assert list(schema.get_schema_errors(str(uuid4()))) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:uuid', 'foobar')]

    def test_format_uri(self):
        schema = StringSchema(format=StringFormat.URI)
        assert list(schema.get_schema_errors("https://foo.com/bar?zap=bang")) == []
        assert list(schema.get_schema_errors("foobar")) == [SchemaError('', 'format:uri', 'foobar')]
