import asyncio
import aiosqlite

async def adding_user(db,name,balance):
        await db.execute("INSERT INTO accounts(name,balance) VALUES (?,?,?)",(name,balance))

async def getting_actualvalue(db,column,table,clue,cluename):
        try :
                             allowed_columns = ["account_id","name","balance","type","status"]
                             allowed_tables = ["accounts","transactions"]
        
                             if column not in allowed_columns or clue not in allowed_columns or table not in allowed_tables:
                                                  raise ValueError("Invalid Column or Table")
        
                             value_cursor = await db.execute(f"SELECT {column} FROM {table} WHERE {clue} = (?)",(cluename,))
                             value_row = value_cursor.fetchone()
                             value = value_row[0]
     
                             return value
        
        except Exception as e:
                               return f"Value extraction failed due to {e}"
                
          

async def withdraw(balance,amount,db,acc_id):
    try :
            if balance > amount:
                     current_balance = balance - amount
                     await db.execute("INSERT INTO transaction(account_id) VALUES (?)",(acc_id,))
                     await db.execute("UPDATE accounts SET balance = (?) WHERE account_id = (?)",(current_balance,),(acc_id,))
                     await db.execute("UPDATE transactions SET type,status = (?,?) WHERE account_id = (?)",("Withdraw","Succes"),(acc_id))
                     await db.commit()
                     return "Withdraw completed"
            else:
                                raise ValueError("You are not eligible for withdraw . Reason :  Amount to withdraw is greater ")
            
    except Exception as e :
                      await db.rollback()
                      await db.execute("UPDATE transactions SET type,status = (?,?) WHERE account_id = (?)",("Withdraw","Failed"),(acc_id))
                      await db.commit()
                      return f"Withdraw failed due to error {e}"
    
async def deposit(balance,amount,db,acc_id):
        try:
                
                balance += amount
                await db.execute("INSERT INTO transaction(account_id) VALUES (?)",(acc_id,))
                await db.execute("UPDATE accounts SET balance = (?) WHERE account_id = (?)",(balance,))
                await db.execute("UPDATE transactions SET type,status = (?,?) WHERE account_id = (?)",("Deposit","Succes"),(acc_id))
                await db.commit()
                return "Deposit completed"
        
        except Exception as e:
                                await db.rollback()
                                await db.execute("UPDATE transactions SET type,status = (?,?) WHERE account_id = (?)",("Deposit","Failed"),(acc_id))
                                await db.commit()
                                return  f"deposit failed due to error {e}"
                
async def transfer(acctr,accre,db,amount):
           
            balance_transfer_acc = getting_actualvalue(db,"balance","accounts","account_id",acctr)
            balance_reciver_acc = getting_actualvalue(db,"balance","accounts","account_id",accre)
            current_balance_transfer_acc = balance_transfer_acc - amount
            current_balance_reciver_acc = balance_reciver_acc + amount
            try :
                        if current_balance_transfer_acc >= 0:
                                  await db.execute("INSERT INTO transaction(account_id) VALUES (?)",(acctr,))
                                  await db.execute("INSERT INTO transaction(account_id) VALUES (?)",(accre,))
                                  await db.execute("UPDATE accounts SET balance = (?) WHERE account_id = (?)",(current_balance_transfer_acc),(acctr))
                                  await db.execute("UPDATE transaction SET type,status = (?,?) WHERE account_id = (?)",("Transfer","Succes"),(acctr,))
                                  await db.execute("UPDATE transaction SET type,status = (?,?) WHERE account_id = (?)",("Transfer","Succes"),(accre,))
                                  await db.execute("UPDATE accounts SET balance = (?) WHERE account_id = (?)",(current_balance_reciver_acc,),(accre,))
                                  await db.commit()
                                  return "Transfer completed"
            except Exception as e :
                                  await db.rollback()
                                  await db.execute("UPDATE transaction SET type,status = (?,?) WHERE account_id = (?)",("Transfer","Failed"),(acctr,))
                                  await db.commit()
                                  return f"Transaction failed due to error {e}"
                                
                


async def process(transaction,amount,name,db,acc_id2name=None):
             try:
                               balance = await getting_actualvalue(db,"balance","accounts","name",name)
                               acc_id = await getting_actualvalue(db,"account_id","accounts","name",name)
                               if transaction.lower() == "withdraw":
                                                check = await withdraw(balance,amount,db,acc_id)
                                                print(check)
                               elif transaction.lower() == "deposit":
                                          check = await deposit(balance,amount,db,acc_id)
                                          print(check)
                               elif transaction.lower() == "transfer":
                                                acc_id2 = getting_actualvalue(db,"account_id","accounts","name",acc_id2name)
                                                check = transfer(acc_id,acc_id2,db,amount)
                                                print("check")
             except Exception as e :
                                        print(f"Error occured in procces.{e}")
                     
                     
async def main():
    async with aiosqlite.connect("Bank.db") as db:
        await db.execute("""
               CREATE TABLE IF NOT EXISTS accounts(
                         account_id INTEGER PRIMARY KEY,
                         name TEXT,
                         balance INTEGER
                        )
                 """)
        await db.commit()
        await db.execute("""
                CREATE TABLE IF NOT EXISTS transactions(
                         transaction_id INTEGER PRIMARY KEY,
                         account_id INTGER,
                         type TEXT,
                         amount TEXT,
                         Status TEXT,
                         
                         )
                 """)
        await db.commit()
        one_person = await adding_user(db,"Adhil",10000)
        fetching = await process("withdraw",5000,"Adhil",db)

asyncio.run(main())
          