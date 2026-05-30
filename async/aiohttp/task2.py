import asyncio
import aiohttp

sem = asyncio.Semaphore(2)

async def web_request(url,session):
    async with sem :
                     async with session.get(url) as response:
                                                   print(f"Url : {url}. Status : {response.status}")

async def all():
      async with aiohttp.ClientSession() as session :
                    await asyncio.gather(
                             web_request("https://google.com",session),
                             web_request("https://github.com",session),
                             web_request("https://wikipedia.org",session),
                             web_request("https://reddit.com",session),
                             web_request("https://stackoverflow.com",session)
                               )
asyncio.run(all())