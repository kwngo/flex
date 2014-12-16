import pytest

from flex.exceptions import ValidationError
from flex.validation.response import (
    validate_response,
)
from flex.error_messages import MESSAGES

from tests.factories import (
    SchemaFactory,
    ResponseFactory,
)
from tests.utils import assert_error_message_equal


def test_response_parameter_validation():
    """
    Test that request validation does parameter validation.  This is largely a
    smoke test to ensure that parameter validation is wired into request
    validation correctly.
    """
    schema = SchemaFactory(
        paths={
            '/get': {
                'get': {
                    'responses': {200: {'description': 'Success'}},
                },
            },
        },
    )

    response = ResponseFactory(url='http://www.example.com/get', status_code=301)

    with pytest.raises(ValidationError) as err:
        validate_response(
            response,
            operation_definition=schema['paths']['/get']['get'],
            context=schema,
            inner=True,
        )

    assert 'status_code' in err.value.messages[0]
    assert_error_message_equal(
        err.value.messages[0]['status_code'][0],
        MESSAGES['response']['invalid_status_code'],
    )
