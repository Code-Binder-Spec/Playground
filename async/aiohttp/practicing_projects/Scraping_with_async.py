import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup

with open("quote.json","w",encoding="utf-8") as f:
                 pass

async def getting_source(url):
        async with aiohttp.ClientSession() as session:
                     async with session.get(url,timeout=aiohttp.ClientTimeout(total=6)) as response:
                                                 return await response.text()
        
async def extracting(url):
         source = await getting_source(url)
         soup = BeautifulSoup(source,"html.parser")
         quotes = soup.select("span.text")
         authors = soup.select("small.author")
         return [{"Quote" : quote.text ,"Author" : author.text } for quote,author in zip (quotes,authors)]
async def all():
        urls = [f"http://quotes.toscrape.com/page/{i}/" for i in range(1,11)]
        result = await asyncio.gather(*[extracting(url) for url in urls])
        data = []
        for page in result:
                for quote in page :
                        data.append(quote)       
        with open("quote.json","a") as f:
                    json.dump(data,f,indent=4) 

asyncio.run(all())
                