import asyncio
from bs4 import BeautifulSoup
import aiohttp
import json

async def getting_source(url):
       async with aiohttp.ClientSession() as session:
              async with session.get(url,timeout=aiohttp.ClientTimeout(total=7)) as response:
                        return await response.text()
              
def extracting_deep_details(titles,scores,comments):
        lis_title = []
        lis_score = []
        lis_comment_count = []
        for title,score,comment in zip(titles,scores,comments) :
                lis_comment_count.append(comment)
                title_name = title.find("a").text
                lis_title.append(title_name)
                score_point = score.text
                lis_score.append(score_point)
                comment = comment.text
                print(f"Title : {title_name} , Score : {score_point} , Comments : {comment}")
                
async def extracting_details(url):
        source = await getting_source(url)
        soup = BeautifulSoup(source,"html.parser")
        titles = soup.find_all("span",class_="titleline")
        scores = soup.find_all("span",class_="score")
        comments_count = [a for a in soup.select(".subline a") if "comments" in a.text]
        extracting_deep_details(titles,scores,comments_count)


asyncio.run(extracting_details("https://news.ycombinator.com/"))
        
