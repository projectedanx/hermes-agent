import asyncio
import time
from urllib.request import urlopen
import json

class MockTrainer:
    def __init__(self):
        self.atropos_api_url = "http://localhost:8080"

    def get_batch_sync(self):
        try:
            with urlopen(f"{self.atropos_api_url}/batch", timeout=10) as response:
                return json.loads(response.read())
        except Exception:
            return {"batch": []}

    async def get_batch_async(self):
        # Without aiohttp, we use asyncio.to_thread
        return await asyncio.to_thread(self.get_batch_sync)

async def get_data_sync_poll(trainer):
    import time
    while True:
        data = trainer.get_batch_sync()
        if data.get("batch"):
            return data
        else:
            time.sleep(1)

async def get_data_async_poll(trainer):
    while True:
        data = await trainer.get_batch_async()
        if data.get("batch"):
            return data
        else:
            await asyncio.sleep(1)

async def test_concurrent_tasks(poll_func):
    trainer = MockTrainer()

    # Track how many times a concurrent task runs
    counter = 0
    async def concurrent_task():
        nonlocal counter
        while True:
            counter += 1
            await asyncio.sleep(0.1)

    # Mock get_batch to simulate waiting for 3 iterations
    calls = 0
    def mock_get_batch(*args):
        nonlocal calls
        calls += 1
        if calls >= 3:
            return {"batch": [1, 2, 3]}
        return {}

    trainer.get_batch_sync = mock_get_batch
    trainer.get_batch_async = lambda: asyncio.to_thread(mock_get_batch)

    # Run both the poll and concurrent task
    task = asyncio.create_task(concurrent_task())
    start = time.time()
    await poll_func(trainer)
    duration = time.time() - start
    task.cancel()

    return duration, counter

async def main():
    print("Testing synchronous polling (blocks event loop):")
    duration, counter = await test_concurrent_tasks(get_data_sync_poll)
    print(f"Duration: {duration:.2f}s, Concurrent task iterations: {counter}")

    print("\nTesting asynchronous polling (allows event loop to run):")
    duration, counter = await test_concurrent_tasks(get_data_async_poll)
    print(f"Duration: {duration:.2f}s, Concurrent task iterations: {counter}")

if __name__ == "__main__":
    asyncio.run(main())
