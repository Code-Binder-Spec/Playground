import asyncio

sem = asyncio.Semaphore(3)

async def treat_patient(name,time):
    async with sem:
           print(f"Patient {name} entering to the room")
           await asyncio.sleep(time)
           print(f"Patient {name} completed the treatment")

async def all():
  
    await asyncio.gather(
        treat_patient("kempachi",3),
        treat_patient("ganju",6),
        treat_patient("tatsuki",5),
        treat_patient("ichigo",4),
        treat_patient("rukia",8),
        treat_patient("kon",1),
        treat_patient("urahara",2),
        treat_patient("orihime",7)
    )

asyncio.run(all())
