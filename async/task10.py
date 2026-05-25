import asyncio

async def mall():
    print("Mall opening")
    await asyncio.sleep(3)
    print("mall closed")

async def carshop():
    print("carshop opened")
    await asyncio.sleep(3)
    print("carshop closed")

async def all():
    task1 = asyncio.create_task(mall())
    task2 = asyncio.create_task(carshop())
    await task2
    await task1

asyncio.run(all())