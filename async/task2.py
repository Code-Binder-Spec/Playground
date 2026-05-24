import asyncio

async def coffee_order(name,time):
    print(f"Making : {name}")
    await asyncio.sleep(time)
    print(f"{name} : ready")

async def calling():
    await asyncio.gather(
        coffee_order("Latte",4),
        coffee_order("cappucino",3),
        coffee_order("espresso",6)
    )

asyncio.run(calling())