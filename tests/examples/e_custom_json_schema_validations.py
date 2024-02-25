from injecty import get_default_injecty_context
from jsonschema import ValidationError

from schemey.json_schema.schema_validator_abc import SchemaValidatorABC
from schemey.validator import validator_from_json


class UniqueNamesValidator(SchemaValidatorABC):
    property_name = "uniqueNames"

    def validate(self, validator, aP, instance, schema):
        """
        A custom validator that ensures that values for the name attribute for items in an array are unique.
        """
        # if not validator.is_type(instance, "array"):
        #    return
        # if not schema.get("uniqueNames"):
        #    return
        names = set()
        for item in instance:
            # if not validator.is_type(item, "object"):
            #    continue  # We assume that type validations are handled elsewhere
            name = item.get("name")
            # if not isinstance(name, str):
            #    continue
            if name in names:
                yield ValidationError(
                    f"Duplicate Name: {name}",
                    validator=validator,
                    validator_value=aP,
                    instance=instance,
                    schema=schema,
                )
            names.add(name)


# We register the validator we just defined
get_default_injecty_context().register_impl(SchemaValidatorABC, UniqueNamesValidator)

json_schema = {
    "type": "array",
    "uniqueNames": True,
    "items": {
        "name": "SomeNamedItem",
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "additionalProperties": False,
    },
}
validator = validator_from_json(json_schema)
validator.validate(
    [
        {"name": "Bill"},
        {"name": "Ted"},
    ]
)
errors = list(
    validator.iter_errors(
        [
            {"name": "Bill"},
            {"name": "Bill"},
        ]
    )
)
print(errors)  # There should be an error here since the name "Bill" is duplicated!
