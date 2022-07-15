from dataclasses import dataclass

_SchemaABC = "schemey.schema_abc.SchemaABC"
_JsonSchemaContext = "schemey.json_schema_context.JsonSchemaContext"


@dataclass
class ParamSchema:
    name: str
    schema: _SchemaABC
    required: bool = True
    param_in: str = "query"

    def dump_json(self, json_context: _JsonSchemaContext):
        return {
            "in": self.param_in,
            "name": self.name,
            "schema": self.schema.dump_json_schema(json_context),
            "required": self.required,
        }
