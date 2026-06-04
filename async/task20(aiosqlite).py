import asyncio
import aiosqlite

async def main():
    db = await aiosqlite.connect("testing.db")
    print("connected")
    await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                     id INTEGER PRIMARY KEY,
                     username TEXT,
                     Perfomance
                      )
""")
    await db.close()

asyncio.run(main())