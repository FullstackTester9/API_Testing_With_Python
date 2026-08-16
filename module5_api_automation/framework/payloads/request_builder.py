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

    def build(self, **values):
        payload = deepcopy(self._template)

        for key, value in values.items():
            if key not in payload:
                raise KeyError(
                    f"Unknown payload field: {key}"
                )

            payload[key] = value

        return payload