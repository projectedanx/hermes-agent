import asyncio
import time
import requests
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential

class MockTrainer:
    def __init__(self):
        self.atropos_api_url = "http://localhost:8080"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15))
    def get_batch_sync(self):
        data = requests.get(f"{self.atropos_api_url}/batch", timeout=10).json()
        return data

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15))
    async def get_batch_async(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.atropos_api_url}/batch", timeout=10) as response:
                response.raise_for_status()
                return await response.json()

if __name__ == "__main__":
    trainer = MockTrainer()
