import asyncio

async def fast():
    print("starting fast")
    await asyncio.sleep(2)
    print("ending fast")

async def slow():
    print("starting slow")
    await asyncio.sleep(5)
    await fast()
    print("ending slow")

async def all():
    await asyncio.gather(
        fast(),
        slow()
)
    
asyncio.run(all())