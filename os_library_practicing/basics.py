import os 

def content_fetcher(path,depth=0):
    if os.path.exists(path):
                      items  = os.listdir(path)
                      for item in items :
                                    full_path = os.path.join(path,item)
                                    indent = "     "*depth

                                    if os.path.isdir(full_path):
                                               print(f"{indent} {item}")
                                               content_fetcher(full_path,depth+1)
                                    else :
                                                print(f"{indent} {item}")
    else :
            print("Path does not exist")

def specific_entry_exist_checker(path):
    if os.path.exists(path):
          if os.path.isdir(path):
               print("Yes the path exist . Its a folder")
          else :
               print("Yes the path exist . Its a file")
    else :
           print("Path does not exist")

       
def fun_for_printing_specific_entry(items,type,path):
        file = None
        folder = None
        if type == "file":
                file = True
        else :
                folder = True
        for item in items :
                full_path = os.path.join(path,item)
                check = os.path.isdir(full_path)
                if check and folder:
                        print(item)
                elif not check and file :
                        print(item)


def specific_entry_lister(path,type): 
     if os.path.exists(path):
            items = os.listdir(path)
            fun_for_printing_specific_entry(items,type,path)

def specific_entry_adder(path,type):
        file_type_list = ["txt", "md", "log", "csv", "env", "yaml", "yml", "py", "sh", "html"]
        try :
                       if type == "file":
                                      file_name = str(input("Enter file name : "))
                                      file_type = str(input("Enter file type [no dot needed].[only text based formats allowed] : "))
                                      if file_type.lower() not in file_type_list:
                                              raise ValueError("The file type you mentioned is invalid . check is it a text based format or it contains dot")
                                      with open(f"{path}/{file_name}.{file_type.lower()}","w") as f:
                                              pass
                       elif type == "folder":
                                      folder_name = str(input("Please enter the folder name : "))
                                      full_path = os.path.join(path,folder_name)
                                      os.mkdir(full_path)
        except Exception as e :
                print(f"error occured while creating . error : {e}")
                                

def entry_remover(path) :
        os.remove(path)
        
                   
cur_path = "/home/coder/coding/Validation-Database-Web-scarping"
specific_entry_exist_checker(cur_path)
content_fetcher(cur_path)
print("content fetcher finished")
specific_entry_lister(cur_path,"folder")




      


      
      