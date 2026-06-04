import asyncio
import aiosqlite

async def creating_table():
       async with aiosqlite.connect("firsttable.db") as db:
                         try:
                                    await  db.execute("""
                                             CREATE TABLE IF NOT EXISTS users(
                                             id INTEGER PRIMARY KEY ,
                                             name TEXT
                                                           )
                                                                 """)
                                    await db.commit()
                                    await db.execute("INSERT INTO users(name) VALUES(?)",("Adhil",))
                                    await db.commit()
                                    users = [("Jon",),("Bob",),("Alice",),("Hasan",)]
                                    await db.executemany("INSERT INTO users(name) VALUES(?,?)",users)
                                    await db.commit()
                         except Exception as e :
                                                    await db.rollback()
                                                    print(e)

asyncio.run(creating_table())