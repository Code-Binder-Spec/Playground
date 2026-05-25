import asyncio

async def file_downloader(filename,size):
      print(f"File : {filename} , Size : {size} , Download Status : started")
      await asyncio.sleep(5)
      print(f"File : {filename} , Size : {size} , Download Status : completed")

async def datbase():
      print("Database started")
      await asyncio.sleep(2)
      print("Database ended")

async def api_call():
      print("Api calling")
      await asyncio.sleep(1)
      print("APi got")

async def all():
             
              file = asyncio.create_task(file_downloader("Onepiece",182))
              data = asyncio.create_task(datbase())
              api = asyncio.create_task(api_call())
              print("All task created")
              await data,file,api

asyncio.run(all())
