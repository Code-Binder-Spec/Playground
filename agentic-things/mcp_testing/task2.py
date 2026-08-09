from mcp.client.stdio import stdio_client
from mcp import ClientSession,StdioServerParameters
import asyncio

async def collecting_data_for_processing():
     collected_num_list = []
     while True:
          try :
                type_of_operation = int(input("Which Type of operation do you need ? \n Here are the options \n 1.Addition \n 2.Subtraction \n 3.Multiplication \n 4.Division \n PLEASE ENTER AN OPTION NUMBER : "))
                if type_of_operation > 4  or type_of_operation < 1:
                         raise ValueError("Invalid operation number detected")
                count_of_number_going_to_type = int(input("How much numbers needed for your calculation ? [Please enter a valid number] : "))
                for i in range(count_of_number_going_to_type):
                       num = float(input("Enter the number : "))
                       collected_num_list.append(num)
                break
          except Exception as e :
                 print(f"Error occured : {e}")
                 continue
     return (type_of_operation,collected_num_list)
                     

async def main():
       server_parametres = StdioServerParameters(
              command="python",
              args=["agentic-things/mcp_testing/task2_tool.py"]
       )
       async with stdio_client(server_parametres) as (read,write):
              async with ClientSession(read,write) as session:
                     await session.initialize()
                     data,num_list = await collecting_data_for_processing()
                     if data == 1:
                           result =  await session.call_tool("addition",{"list_name":num_list})
                     elif data == 2 :
                           result = await session.call_tool("substraction",{"list_name":num_list})
                     elif data == 3:
                            result = await session.call_tool("multiplication",{"list_name":num_list})
                     elif data == 4 :
                            result = await session.call_tool("division",{"list_name":num_list})
                     print(result.content[0].text)

if __name__ == "__main__":
       asyncio.run(main())
                            
              
       
