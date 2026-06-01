import asyncio
from bs4 import BeautifulSoup
import aiohttp
import json

async def getting_source(url):
       async with aiohttp.ClientSession() as session:
              async with session.get(url,timeout=aiohttp.ClientTimeout(total=7)) as response:
                        return await response.text()
              
def score_scraping(soup):
        scores = [score.text for score in soup.select("span.score")]
        return scores

def title_scraping(soup):
        titles = []
        for title in soup.select("span.titleline a"):
                titles.append(title.text)
        return titles

def comment_scraping(soup):
        comments = []
        for comment in soup.select("span.subline a"):
                if "comment" in comment.text:
                        comments.append(comment.text)
                else :
                        comments.append("No comments")
        return(comments)

async def all_function_calling(soup):
           scores =  score_scraping(soup)
           titles =title_scraping(soup)
           comments = comment_scraping(soup)
           return [{"Title" : title ,"Score"  : score,"Comment count" : comment } for title,score,comment in zip(titles,scores,comments)]

async def passing_soup(url):
        source = await getting_source(url)
        soup = BeautifulSoup(source,"html.parser")
        result = await all_function_calling(soup)
        return result

async def main():
        urls = [f"https://news.ycombinator.com/?p={i}" for i in range(1,31) ]
        result = await asyncio.gather(*[passing_soup(url) for url in urls])
        with open("Hackernews.json","w",encoding="utf-8") as f:
                   full_data = []
                   for page in result:
                                     for details in page:
                                             full_data.append(details)
                   json.dump(full_data,f,indent=4)
                                             

asyncio.run(main())


        
