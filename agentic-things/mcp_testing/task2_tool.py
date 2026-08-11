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
    divided = 0
    try :
         for i in range(len(list_name)):
             if i == 0:
                       divided = list_name[i]/list_name[i+1]
             elif i == 1:
                   continue
             else :
                  divided = divided/list_name[i]
    except Exception as e :
              divided = f"Error occured : {e}"
    return divided

if __name__ == "__main__":
     mcp.run()



        
    


