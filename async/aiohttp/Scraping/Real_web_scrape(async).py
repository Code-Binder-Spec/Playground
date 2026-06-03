import asyncio
from bs4 import BeautifulSoup
import aiohttp
import json

sem = asyncio.Semaphore(3)

async def getting_source(url,session):
       try :
              async with sem :
                      async with session.get(url,timeout=aiohttp.ClientTimeout(total=7)) as response:
                                return await response.text()
       except Exception as e  :
                    return e
              
def score_scraping(trs2):
        if trs2.find("span",class_="score"):
                    score = trs2.find("span",class_="score").text
        else :
                score = "0 point"
        return score

def title_scraping(soup):
        if soup.find("span",class_="titleline").find("a"):
                title = soup.find("span",class_="titleline").find("a").text
        else :
                title = "missing"
        print(title)
        return title

def comment_scraping(trs2):
        if trs2.find("span",class_="subline"):
                if len(trs2.find("span",class_="subline").find_all("a")) > 2:
                                comment = trs2.find("span",class_="subline").find_all("a")[3].text
                else :
                                comment = "discuss"
        else : 
                comment = "discuss"
        return comment

async def all_function_calling(trs,trs2):
           score =  score_scraping(trs2)
           title = title_scraping(trs)
           comment = comment_scraping(trs2)
           return {"Title" : title ,"Score"  : score , "comment" : comment} 

async def passing_soup(url,session):
        source = await getting_source(url,session)
        if isinstance(source,Exception):
                return [f"url : {url} failed to fecth details due to {source}"]
        soup = BeautifulSoup(source,"html.parser")
        athing_submission = soup.find_all("tr",class_="athing submission")
        lis_data = []
        for tr1 in athing_submission:
                 tr2 = tr1.find_next_sibling("tr")
                 data = await all_function_calling(tr1,tr2)
                 lis_data.append(data)
        return lis_data
async def main():
         async with aiohttp.ClientSession() as session:
                 urls = [f"https://news.ycombinator.com/?p={i}" for i in range(1,31) ]
                 result = await asyncio.gather(*[passing_soup(url,session) for url in urls])
                 print(result)
                 full_data = []
                 with open("Hackernews.json","w",encoding="utf-8") as f:
                           for page in result:
                                        for details in page:
                                                full_data.append(details)
                           json.dump(full_data,f,indent=4)
asyncio.run(main())


        
