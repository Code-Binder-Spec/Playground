import asyncio

async def task_a():
    await asyncio.sleep(5)
    print("ended a ")

async def task_b():
    await asyncio.sleep(2)
    print("ending b")

async def task_c():
    await asyncio.sleep(1)
    print("ending c ")

async def main():
    await asyncio.gather(
        task_a(),
        task_b(),
        task_c()
    )

asyncio.run(main())