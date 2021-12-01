import pytest

from .helpers import EXAMPLE_DATA_3, mock_responses


@pytest.fixture
def default_stars_response():
    with mock_responses(EXAMPLE_DATA_3, require_all=False) as r:
        yield r
