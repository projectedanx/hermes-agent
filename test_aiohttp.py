import aiohttp
import asyncio

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            print("aiohttp initialized successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
