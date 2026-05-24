import asyncio

async def greet():
    print("hello")
    await asyncio.sleep(2)
    print("hi")

async def greet2():
    print("during 1 ")
    await asyncio.sleep(1)
    print("after 3")

async def main():
    await asyncio.gather( greet(),
                    greet2()
                                   )
asyncio.run(main())