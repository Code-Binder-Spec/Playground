import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session :
           async with session.get(url) as response:
                     print(f"url : {url} . status : {response.status}")

asyncio.run(fetch("https://google.com"))