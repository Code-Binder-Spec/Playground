import os 

current_path = os.getcwd()
print(type(current_path))

datas = []

def collecting_data(list_var):
      for folder,subfolder,file in os.walk(current_path):
            list_var.append((folder,subfolder,file))

collecting_data(datas)

def doing_printing_job(index_num,lis_var,word):
       check_object = lis_var[index_num]
       if check_object:
             print(word," : \n")
             singular = word[:-1]
             for i in range(len(check_object)):
                   print(f"{singular} {i+1} : {check_object[i]}")
       else :
             print(f"{word} : Empty")


for data in datas:
      if data:
               print(f"\nFolder : {data[0]}")
               sub_folder = data[1]
               files = data[2]
               doing_printing_job(1,data,"Subfolders")
               doing_printing_job(2,data,"Files")
      else :
             continue


      


      
      