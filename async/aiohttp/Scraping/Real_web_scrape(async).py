import asyncio
from bs4 import BeautifulSoup
import aiohttp
import json
import logging

logging.basicConfig(filename="Hackernews.log",level=logging.DEBUG)

sem = asyncio.Semaphore(3)

async def getting_source(url,session):
       try :
              async with sem :
                      async with session.get(url,timeout=aiohttp.ClientTimeout(total=7)) as response:
                                status_code = response.status
                                if status_code == 200:
                                         return await response.text()
                                else :
                                        raise Exception("Bad status not eligible for scraping")
       except Exception as e  :
                                 return e
              
def score_scraping(trs2):
        score_check = trs2.find("span",class_="score")
        if score_check:
                    score =score_check.text
        else :
                score = "0 point"
        return score

def title_scraping(soup):
        title_check = soup.find("span",class_="titleline")
        if title_check:
                title = title_check.find("a").text
        else :
                title = "missing"
        return title

def comment_scraping(trs2):
        comment_check = trs2.find("span",class_="subline")
        if comment_check :
                comment_count = comment_check.find_all("a")
                if len(comment_count) > 2:
                                comment =  comment_count[3].text
                else :
                                comment = "discuss"
        else : 
                comment = "discuss"
        return comment

def extract_story(trs,trs2):
           score =  score_scraping(trs2)
           title = title_scraping(trs)
           comment = comment_scraping(trs2)
           return {"Title" : title ,"Score"  : score , "comment" : comment} 

async def passing_soup(url,session):
        source = await getting_source(url,session)
        if isinstance(source,Exception):
                logging.error(f"{url} : Fetched failed . Reason : {source}")
                return []
        logging.info(f"{url} : fetched succeed securely.")
        soup = BeautifulSoup(source,"html.parser")
        athing_submission = soup.find_all("tr",class_="athing submission")
        lis_data = []
        for tr1 in athing_submission:
                 tr2 = tr1.find_next_sibling("tr")
                 data = extract_story(tr1,tr2)
                 lis_data.append(data)
        return lis_data

def save_file(fulldata):
        with open("Hackernews.json","w",encoding="utf-8") as f:
                json.dump(fulldata,f,indent=4)

async def main():
         async with aiohttp.ClientSession() as session:
                 urls = [f"https://news.ycombinator.com/?p={i}" for i in range(1,31) ]
                 result = await asyncio.gather(*[passing_soup(url,session) for url in urls])
                 full_data = []
                 for page in result:
                          for details in page:
                                    full_data.append(details)
                 save_file(full_data)
asyncio.run(main())


        
