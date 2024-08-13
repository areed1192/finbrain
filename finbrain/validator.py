import json
from jsonschema import validate
from jsonschema import ValidationError


class Validator:

    def validate_json_schema(self, json_string: str, schema: dict) -> dict:
        """Validates a JSON string against a JSON schema.

        ### Parameters:
        ----
        json_string: str
            The JSON string to be validated.

        schema: dict
            The JSON schema to validate the JSON string against.

        ### Returns:
        ----
        dict:
            The JSON object if the JSON string is valid, otherwise an empty dictionary.

        ### Raises:
        ----
        json.JSONDecodeError:
            If the JSON string is invalid.

        ValidationError:
            If the JSON string does not match the schema.
        """
        try:
            json_obj = json.loads(json_string)
            validate(instance=json_obj, schema=schema)
            return {
                "status": "success",
                "message": "JSON object is valid",
                "object": json_obj
            }
        except (json.JSONDecodeError, ValidationError) as e:
            return {
                "status": "error",
                "message": f"Invalid JSON object: {e}",
                "object": json_string
            }
