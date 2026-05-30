import asyncio

sem = asyncio.Semaphore(3)

async def car_washing(car,time):
    async with sem:
                  print(f"{car} washing started")
                  await asyncio.sleep(time)
                  print(f"{car} washing completed")

async def all():
       results = await asyncio.gather(
                car_washing("ferrari",4),
                car_washing("lambhorgini",3),
                car_washing("porshe",2),
                car_washing("bmw","none"),
                car_washing("mustang",5),
                car_washing("supra",7),
                car_washing("rolls royce",9),
                car_washing("buggatti",8),
                return_exceptions=True

        )
      
       for i,result in enumerate(results):
               if isinstance(result,Exception):
                       print(f"Task {i+1}. Stauts : failed")
               else :
                     print(f"Task {i+1}. Stauts : completed")  
                        
       
        
    
asyncio.run(all())

       


