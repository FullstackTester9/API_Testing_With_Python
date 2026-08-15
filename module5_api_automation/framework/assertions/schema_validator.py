from jsonschema import Draft202012Validator


class SchemaValidator:

    @staticmethod
    def validate_json(response, schema):

        response_data = response.json()

        validator = Draft202012Validator(schema)

        errors = sorted(
            validator.iter_errors(response_data),
            key=lambda error: list(error.path)
        )

        if errors:

            messages = []

            for error in errors:

                path = ".".join(
                    str(item)
                    for item in error.path
                )

                if not path:
                    path = "<root>"

                messages.append(
                    f"{path}: {error.message}"
                )

            raise AssertionError(
                "JSON Schema validation failed:\n"
                + "\n".join(messages)
            )

    @staticmethod
    def validate_json_data(data, schema):

        validator = Draft202012Validator(schema)

        errors = sorted(
            validator.iter_errors(data),
            key=lambda error: list(error.path)
        )

        if errors:

            messages = []

            for error in errors:

                path = ".".join(
                    str(item)
                    for item in error.path
                )

                if not path:
                    path = "<root>"

                messages.append(
                    f"{path}: {error.message}"
                )

            raise AssertionError(
                "JSON Schema validation failed:\n"
                + "\n".join(messages)
            )