import pytest
from .helpers import mock_responses, EXAMPLE_DATA_3

@pytest.fixture
def default_stars_response():
    with mock_responses(EXAMPLE_DATA_3, require_all=False) as r:
        yield r
