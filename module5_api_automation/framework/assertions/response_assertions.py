class ResponseAssertions:

    # ==================================================
    # Status code assertions
    # ==================================================
    @staticmethod
    def assert_status_code(response, expected_status_code):
        actual_status_code = response.status_code

        assert actual_status_code == expected_status_code, (
            f"Expected status code {expected_status_code}, "
            f"but received {actual_status_code}"
        )

    # ==================================================
    # Content-Type assertions
    # ==================================================
    @staticmethod
    def assert_json_content_type(response):
        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        assert "application/json" in content_type, (
            "Expected JSON content type, "
            f"but received '{content_type}'"
        )

    # ==================================================
    # Response JSON assertions
    # ==================================================
    @staticmethod
    def assert_response_is_json(response):

        try:
            response.json()

        except ValueError:
            raise AssertionError(
                "Response body is not valid JSON."
            )

    # ==================================================
    # JSON field assertions
    # ==================================================
    @staticmethod
    def assert_json_field_exists(response, field_name):

        response_data = response.json()

        assert field_name in response_data, (
            f"Expected JSON field '{field_name}' "
            "was not found in the response."
        )

    # ==================================================
    # JSON field value assertions
    # ==================================================
    @staticmethod
    def assert_json_field_value(
            response,
            field_name,
            expected_value
    ):

        response_data = response.json()

        assert field_name in response_data, (
            f"JSON field '{field_name}' "
            "was not found in the response."
        )

        actual_value = response_data[field_name]

        assert actual_value == expected_value, (
            f"Expected '{field_name}' to be "
            f"'{expected_value}', "
            f"but received '{actual_value}'."
        )

    # ==================================================
    # JSON field type assertions
    # ==================================================
    @staticmethod
    def assert_json_field_type(
            response,
            field_name,
            expected_type
    ):

        response_data = response.json()

        assert field_name in response_data, (
            f"JSON field '{field_name}' "
            "was not found in the response."
        )

        actual_value = response_data[field_name]

        assert isinstance(actual_value, expected_type), (
            f"Expected '{field_name}' to be of type "
            f"{expected_type.__name__}, "
            f"but received {type(actual_value).__name__}."
        )

    # ==================================================
    # Response header assertions
    # ==================================================
    @staticmethod
    def assert_header_exists(response, header_name):

        assert header_name in response.headers, (
            f"Expected response header "
            f"'{header_name}' was not found."
        )

    # ==================================================
    # Response header value assertions
    # ==================================================
    @staticmethod
    def assert_header_value(
            response,
            header_name,
            expected_value
    ):

        actual_value = response.headers.get(header_name)

        assert actual_value == expected_value, (
            f"Expected header '{header_name}' "
            f"to have value '{expected_value}', "
            f"but received '{actual_value}'."
        )

    # ==================================================
    # Response time assertions
    # ==================================================
    @staticmethod
    def assert_response_time_less_than(
            response,
            maximum_seconds
    ):

        assert response.elapsed.total_seconds() < maximum_seconds, (
            f"Expected response time to be less than "
            f"{maximum_seconds} seconds, "
            f"but actual response time was "
            f"{response.elapsed.total_seconds():.3f} seconds."
        )

