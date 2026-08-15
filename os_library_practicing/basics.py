import os 
from groq import Groq
from dotenv import load_dotenv


groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def calling_ai(client):
                  while True :
                                 chunk = str(input("what are you looking for ? please enter the path of file or folder . : "))
                                 message = client.chat.completions.create(
                                                  model="llama-3.3-70b-versatile",
                                                  max_tokens=1024,
                                                  messages= [
                                                               {"role":"user","content": f"Context : {chunk}\n\nInstructions : You are a File Path Extractor. Read the user's message and construct a Linux-style absolute file path based on locations mentioned, outermost first, going deeper as more detail is given. If only one top-level location is mentioned, return that alone as the full path. If no identifiable path or location is mentioned at all, respond with exactly: No path found, please try again. Do not explain your reasoning, add commentary, or guess/hallucinate folder names that were not stated or clearly implied. Output ONLY the final path or the exact no-path message, nothing else, using standard Linux path conventions with forward slashes."}
                                                            ]
                                      )
                                 current_path = message.choices[0].message.content
                                 if os.path.exists(current_path):
                                              break
                                 print("Path didnt found try again")
                  return current_path


def collecting_data(list_var,current_path):
                        for folder,subfolder,file in os.walk(current_path,topdown=False):
                                               list_var.append((folder,subfolder,file))

def doing_printing_job(index_num,lis_var,word):
                  check_object = lis_var[index_num]
                  if check_object:
                              print(word," : ")
                              singular = word[:-1]
                              for i in range(len(check_object)):
                                           print(f"{singular} {i+1} : {check_object[i]}")
                  else :
                                          print(f"{word} : Empty")

def checking_what_is_in_the_folder():

                    datas = []
                    path = calling_ai(groq_client)
                    collecting_data(datas,path)
                    for data in datas:
                                           print(f"\nFolder : {data[0]}")
                                           doing_printing_job(1,data,"Subfolders")
                                           doing_printing_job(2,data,"Files")

checking_what_is_in_the_folder()


      


      
      