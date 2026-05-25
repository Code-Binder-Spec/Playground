import asyncio

async def creation_task_1(a,b):
       print("starting sum calculation")
       c = a+b
       await asyncio.sleep(2)
       print(f"{a}+{b} = {c}")

async def creation_task2(a,b):
       print("starting substracting calculation")
       c = a-b
       await asyncio.sleep(3)
       print(f"{a}-{b} = {c}")


async def all():
                    sub = asyncio.create_task(creation_task2(10,5))
                    print("Substract task created ")
                    await sub
                    ad = asyncio.create_task(creation_task_1(9,4))
                    print("addition task created")
                    await ad

asyncio.run(all())