from mcp.server import MCPServer


mcp = MCPServer("calculator tools")

@mcp.tool()
def addition(list_name):
    "Addition of the numbers"
    num_sum = 0
    for i in list_name:
        num_sum += i
    return num_sum

@mcp.tool()
def substraction(list_name):
    "Subtraction of numbers"
    first_num = list_name[0]
    list_name.remove(list_name[0])
    sub_sum = 0
    for i in list_name:
        sub_sum += i
    subbed_answer = first_num-sub_sum
    return subbed_answer

@mcp.tool()
def multiplication(list_name):
    "Multiplication of numbers"
    multiplied = 1
    for i in list_name:
        multiplied *= i
    return multiplied

@mcp.tool()
def division(list_name):
    base = 1
    divided = 0
    try :
         for i in list_name:
             divided = i/base
             base = i
    except Exception as e :
             divided = f"Error occured : {e}"
    return divided

if __name__ == "__main__":
     mcp.run()



        
    


