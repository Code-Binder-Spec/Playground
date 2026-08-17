import os 
def content_fetcher(path,depth=0):
    if os.path.exists(path):
                      items  = os.listdir(path)
                      for item in items :
                                    full_path = os.path.join(path,item)
                                    indent = "     "*depth

                      if os.path.isdir(full_path):
                            print(f"{indent} {item}")
                            content_fetcher(full_path,depth=1)
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

       

def specific_entry_lister(path,type):
     if os.path.exists(path):
            items = os.listdir(path)
            if type == "file":
                   for item in items:
                          full_path = os.path.join(path,item)
                          if os.path.isdir(full_path):
                                 continue
                          else :
                                 print("item")
            elif type == "folder":
                   for item in items:
                          full_path = os.path.join(path,item)
                          if os.path.isdir(full_path):
                                 print(item)
                          else :
                                 continue
                   
                   

cur_path = str(input("Enter current path : "))
content_fetcher(cur_path)


      


      
      