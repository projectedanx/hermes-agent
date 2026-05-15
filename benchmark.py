import asyncio
import time
import requests
import aiohttp

# We'll just test the get_data function mock
from tinker_atropos.trainer import TinkerAtroposTrainer
from tinker_atropos.config import TinkerAtroposConfig

config = TinkerAtroposConfig(
    base_model="test",
    atropos_api_url="http://localhost:8080",
)

trainer = TinkerAtroposTrainer(config)

async def test_blocking():
    # we need a mock server
    pass
