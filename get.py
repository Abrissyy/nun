import asyncio
import aiohttp
import time
import sys
from urllib.parse import urlparse

async def send_get_request(session, url):
    try:
        async with session.get(url) as response:
            print(f"GET request to {url} - Status code: {response.status}")
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")

async def worker(url, end_time):
    async with aiohttp.ClientSession() as session:
        while time.time() < end_time:
            await send_get_request(session, url)

async def main():
    if len(sys.argv) != 4:
        print("Usage: python get.py <url> <time> <port>")
        sys.exit(1)

    url = sys.argv[1]
    duration = float(sys.argv[2])
    port = int(sys.argv[3])

    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("Invalid URL")
        sys.exit(1)

    full_url = f"{parsed_url.scheme}://{parsed_url.hostname}:{port}{parsed_url.path}"

    end_time = time.time() + duration
    tasks = []

    for _ in range(500):
        tasks.append(worker(full_url, end_time))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
