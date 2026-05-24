import asyncio

async def getting_content(filename,size):
    if size > 10 :
               time = size / 10
               print("Downloading started ")
               await asyncio.sleep(time)
               print(f"{filename} : Downloaded ")
    else :
            print("File size must be more than 10")

async def gathered():
        await asyncio.gather(
                getting_content("Naruto ep 1",100),
                getting_content("one piece ep 152",150),
                getting_content("bleach",90)
        )

asyncio.run(gathered())