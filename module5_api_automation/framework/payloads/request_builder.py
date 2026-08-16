# =====================================================
# Reason for "deepcopy()" -> One test should not
# accidentally modify the original template.
# "RequestBuilder" builds the request using templates
# for the payload.
# =====================================================

from copy import deepcopy


class RequestBuilder:

    def __init__(self, template):
        self._template = deepcopy(template)

    # =====================================================
    # Creates initial payload.
    # =====================================================
    def build(self, **values):
        payload = deepcopy(self._template)

        for key, value in values.items():
            if key not in payload:
                raise KeyError(
                    f"Unknown payload field: {key}"
                )

            payload[key] = value

        return payload

    # =====================================================
    # Modify selected fields of an existing payload.
    # =====================================================
    def override(self, payload, **overrides):
        updated_payload = deepcopy(payload)

        for key, value in overrides.items():
            if key not in updated_payload:
                raise KeyError(
                    f"Unknown payload field: {key}"
                )

            updated_payload[key] = value

        return updated_payload

    # =====================================================
    # Generic payload operation not specific to any module.
    # "set_nested" is used when nested field already exist.
    # =====================================================
    def set_nested(self, payload, path, value):
        updated_payload = deepcopy(payload)

        keys = path.split(".")
        current = updated_payload

        for key in keys[:-1]:

            if key not in current:
                raise KeyError(
                    f"Unknown nested payload field: {path}"
                )

            if not isinstance(current[key], dict):
                raise TypeError(
                    f"Cannot traverse non-object field: {key}"
                )

            current = current[key]

        final_key = keys[-1]

        if final_key not in current:
            raise KeyError(
                f"Unknown nested payload field: {path}"
            )

        current[final_key] = value

        return updated_payload

    # =====================================================
    # "add_optional" is used when when we want add a field
    # that may not currently exist.
    # =====================================================
    def add_optional(self, payload, path, value):
        updated_payload = deepcopy(payload)

        keys = path.split(".")
        current = updated_payload

        for key in keys[:-1]:

            if key not in current:
                current[key] = {}

            if not isinstance(current[key], dict):
                raise TypeError(
                    f"Cannot traverse non-object field: {key}"
                )

            current = current[key]

        current[keys[-1]] = value

        return updated_payload

    # =====================================================
    # "remove_optional" is used when a test needs to remove
    # an optional field.
    # =====================================================
    def remove_optional(self, payload, path):
        updated_payload = deepcopy(payload)

        keys = path.split(".")
        current = updated_payload

        for key in keys[:-1]:

            if key not in current:
                return updated_payload

            if not isinstance(current[key], dict):
                raise TypeError(
                    f"Cannot traverse non-object field: {key}"
                )

            current = current[key]

        current.pop(keys[-1], None)

        return updated_payload