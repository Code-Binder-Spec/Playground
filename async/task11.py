import asyncio

async def school(size):
            print("School opened")
            await asyncio.sleep(size)
            print("School ended")

async def restaurant():
      print("restaurant opened")
      await asyncio.sleep(1)
      print("restaurant closed")
      
async def all ():
      await asyncio.gather(
            
            school("schol"),
            restaurant(),
            return_exceptions=True
      )

asyncio.run(all())