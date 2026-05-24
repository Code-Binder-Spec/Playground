import asyncio

async def fast():
    print("fast started ")
    await asyncio.sleep(1)
    print("fast ended")\
    
async def fast2():
    print("fast2 started")
    await asyncio.sleep(2)
    print("fast2 ended")

async def slow():
    print("slow started")
    await asyncio.sleep(3)
    await fast()
    await fast2()
    print("Slow ended")

async def gathered():
    await asyncio.gather(
        fast(),
        fast2(),
        slow()
    ) 

asyncio.run(gathered())