import asyncio

sem = asyncio.Semaphore(2)

async def watch_fixing(name,damage,time):
    async with sem:
            print(f"Watch {name} started to fix")
            await asyncio.sleep(time)
            print(f"Watch {name} with damage {damage} fixed properly")

async def all():
      w1 = asyncio.create_task(watch_fixing("Casio","Water inside",6))
      w2 = asyncio.create_task(watch_fixing("Rolex","Pin not moving",4))
      w3 = asyncio.create_task(watch_fixing("omega","Battery dead",3))
      w4 = asyncio.create_task(watch_fixing("selko","Touch not working",2))
      w5 = asyncio.create_task(watch_fixing("K-sport","Display broken",5))
      w6 = asyncio.create_task(watch_fixing("Tissot","Button not working",1))

      print("All task created")

      await w2
      await w1
      await w3
      await w4
      await w5
      await w6

asyncio.run(all())