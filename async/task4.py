import asyncio

async def grill():
    print("Grilling started")
    await asyncio.sleep(5)
    print("Grilling ended")

async def salad():
    print("salad making started")
    await asyncio.sleep(2)
    print("Salad making finished")

async def soup():
    print("soup making salad")
    await asyncio.sleep(3)
    print("soup ready")

async def desert():
    print("Desert making started")
    await asyncio.sleep(1)
    print("Desert served ")

async def all():
    await asyncio.gather(
        grill(),
        salad(),
        soup(),
        desert()
)
    
asyncio.run(all())