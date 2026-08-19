import os 

def content_fetcher(path,depth=0):
    if os.path.exists(path):
                      items  = os.listdir(path)
                      for item in items :
                                    full_path = os.path.join(path,item)
                                    indent = "     "*depth

                                    if os.path.isdir(full_path):
                                               print(f"{indent} {item}")
                                               depth += 1
                                               content_fetcher(full_path,depth)
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
        check = None
        if type == "file":
                check = False
        else :
                check = True
        for item in items :
                full_path = os.path.join(path,item)
                if os.path.isdir(full_path):
                        if check:
                                print(item)
                else :
                        continue


def specific_entry_lister(path,type):
     if os.path.exists(path):
            items = os.listdir(path)
            if type == "file":
                   for item in items:
                          full_path = os.path.join(path,item)
                          if os.path.isdir(full_path):
                                 continue
                          else :
                                 print(item)
            elif type == "folder":
                   for item in items:
                          full_path = os.path.join(path,item)
                          if os.path.isdir(full_path):
                                 print(item)
                          else :
                                 continue
                   
                   

cur_path = str(input("Enter current path : "))
specific_entry_exist_checker(cur_path)
content_fetcher(cur_path)
print("content fetcher finished")
specific_entry_lister(cur_path,"file")




      


      
      