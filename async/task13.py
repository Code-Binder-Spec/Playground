import asyncio

sem = asyncio.Semaphore(3)

async def web1(url):
    
    async with sem:
                 print(f"{url} scraping started")
                 await asyncio.sleep(1)
                 print(f"{url} scraping ended")

async def all():
    await asyncio.gather(
            web1("google.com"),
            web1("reddit.com"),
            web1("github.com"),
            web1("youtube.com"),
            web1("twitter.com"),
            web1("netflix.com"),
            web1("amazon.com"),
            web1("wikipedia.com"),
            web1("stackoverflow.com"),
            web1("medium.com")    
            )

asyncio.run(all())
    