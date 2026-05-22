import pytest
import asyncio
import aiohttp
from unittest.mock import patch, MagicMock
from aioresponses import aioresponses

import benchmark

@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m

@pytest.mark.asyncio
async def test_test_blocking(mock_aioresponse):
    # Setup mock aioresponse
    mock_aioresponse.get('http://localhost:8080/v1/health', status=200, payload={"status": "ok"})
    mock_aioresponse.post('http://localhost:8080/v1/completions', status=200, payload={"choices": [{"text": "hello"}]})

    # Assert that no exception is thrown when we call it
    assert hasattr(benchmark, 'test_blocking')
    await benchmark.test_blocking()
