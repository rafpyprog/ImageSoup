import pytest

from imagesoup import parameters as pr


@pytest.mark.parameters
def test_query_buider():
    QUERY = "python"
    EXPECTED_URL = f'https://www.google.com/search?tbm=isch&ijn=0&q={QUERY}'
    query_url = pr.query_builder(QUERY)
    assert query_url == EXPECTED_URL
