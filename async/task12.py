import asyncio
sem = asyncio.Semaphore(5)
async def electroincs():
    async with sem:
        print("electronics started")
        await asyncio.sleep(6)
        print("Electronics ended")

asyncio.run(electroincs())