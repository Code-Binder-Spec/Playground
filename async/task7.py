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

              ad = asyncio.create_task(creation_task_1(6,4))
              sub = asyncio.create_task(creation_task2(7,1))
              print("Both object created ")
              await sub,ad
                           
asyncio.run(all())