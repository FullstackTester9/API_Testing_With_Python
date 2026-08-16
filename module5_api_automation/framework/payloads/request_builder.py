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