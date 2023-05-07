"""
Add a custom validation rule for ranges to json object schema.
e.g.:

{
    "type": "object",
    "properties": {
        "min_value": {"type": "integer", "minimum": 5},
        "max_value": {"type": "integer"}
    },
    "required": ["min_value", "max_value"],
    "ranges": [{
        "minProperty": "min_value",
        "maxProperty": "max_value",
        "allowEqual": false
    }]
}
"""
from jsonschema import ValidationError


def ranges(validator, aP, instance, schema):
    if not validator.is_type(instance, "object"):
        return
    ranges_ = schema.get("ranges") or []
    for range_ in ranges_:
        min_property = range_["minProperty"]
        max_property = range_["maxProperty"]
        allow_equal = range_.get("allowEqual")
        min_value = instance.get(min_property)
        max_value = instance.get(max_property)
        if min_value < max_value:
            continue
        if allow_equal and min_value == max_value:
            continue
        # pylint: disable=R0801
        yield ValidationError(
            f"Value not in future: {instance}",
            validator=validator,
            validator_value=aP,
            instance=instance,
            schema=schema,
        )
