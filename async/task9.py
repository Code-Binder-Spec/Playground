import asyncio

async def library():
    print("Library opened")
    await asyncio.sleep(4)
    print("library closed")

async def theatre():
    print("theatre opened")
    await asyncio.sleep(2)
    print("Theatre close")

async def all():
    lib = asyncio.create_task(library())
    print("calcultaion started")
    thea = asyncio.create_task(theatre())
    print("claculation proccessing")
    await thea
    print("Claculation almost")
    await lib 
    print("Calculation result : 78")

asyncio.run(all())