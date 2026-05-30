import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def getting_source(url):
        async with aiohttp.ClientSession() as session:
                     async with session.get(url,timeout=aiohttp.ClientTimeout(total=4)) as response:
                                                 return await response.text()
        
async def extracting(url):
         source = await getting_source(url)
         soup = BeautifulSoup(source,"html.parser")
         qoutes = soup.select("span.text")
         authors = soup.select("small.author")
         for qoute,author in zip(qoutes,authors):
                 print(f"\n Qoute : {qoute.text} . Author : {author.text}")

async def all():
        urls = [f"http://quotes.toscrape.com/page/{i}/" for i in range(1,11)]
        await asyncio.gather(*[extracting(url) for url in urls])
        
asyncio.run(all())
                