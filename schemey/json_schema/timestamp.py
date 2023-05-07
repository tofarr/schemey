"""
Add a custom date validation rule to json object schema.
e.g.:

{
    "type": "string",
    "format": "date-time",
    "timestamp": {
        "past": true,
        gracePeriodSeconds: 3600
    }
}

{
    "type": "string",
    "format": "date",
    "timestamp": {
        "past": false
    }
}

"""
from datetime import datetime, timezone

from jsonschema import ValidationError


def timestamp(validator, aP, instance, schema):
    """
    Check a timestamp. If times are not specified, it is assumed to be utc.
    """
    format_ = schema.get("format")
    if format_ not in ("date-time", "date"):
        yield ValidationError(
            f"Not a date / date-time: {schema}",
            validator=validator,
            validator_value=aP,
            instance=instance,
            schema=schema,
        )
        return
    timestamp_ = schema["timestamp"]
    now = datetime.now(tz=timezone.utc)
    value = datetime.fromisoformat(instance)
    if not value.tzinfo:
        value = value.replace(tzinfo=timezone.utc)
    if format_ == "date":
        now.replace(hour=0, minute=0, second=0, microsecond=0)
        value.replace(hour=0, minute=0, second=0, microsecond=0)
    now = now.timestamp()
    value = value.timestamp()

    grace_period_seconds = timestamp_.get("gracePeriodSeconds") or 0
    past = timestamp_.get("past")
    if past:
        if value > (now + grace_period_seconds):
            yield ValidationError(
                f"Value not in past: {instance}",
                validator=validator,
                validator_value=aP,
                instance=instance,
                schema=schema,
            )
    else:
        if value < (now - grace_period_seconds):
            # pylint: disable=R0801
            yield ValidationError(
                f"Value not in future: {instance}",
                validator=validator,
                validator_value=aP,
                instance=instance,
                schema=schema,
            )
