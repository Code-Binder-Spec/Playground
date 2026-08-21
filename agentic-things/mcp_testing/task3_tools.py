from mcp.server import MCPServer
import os

mcp = MCPServer("file helper tools")

def checking_path_exist(path):
        if os.path.exists(path):
                pass
        else :
                raise ValueError("Path doesnt exist")


def function_for_content_fetcher(path:str,file_connection,depth:int=0):               
                              items  = os.listdir(path)
                              for item in items :
                                     full_path = os.path.join(path,item)
                                     indent = "     "*depth

                                     if os.path.isdir(full_path):
                                               file_connection.write(f"\n{indent} {item}")
                                               function_for_content_fetcher(full_path,file_connection,depth+1)
                                     else :
                                                file_connection.write(f"\n{indent} {item}")


@mcp.tool()
def content_fetcher(path:str):
    "Recursively lists all files and subfolders inside the given directory path, including everything nested at any depth, and returns the result as an indented tree structure showing the folder hierarchy. Takes a single argument: the folder path to start from."
    data = None
    try:
                      checking_path_exist(path)
                      with open(os.path.join(path,"Content_tree.txt"),"a+") as f :
                              function_for_content_fetcher(path,f)
                              text = f.read()
                              data = text
    except Exception as e :
            data = f"error occured . error : {e}"

    return data 


@mcp.tool()
def specific_entry_exist_checker(path:str):
    "Checks whether a given path exists on the filesystem, and if it does, reports whether it is a file or a folder."
    data = None
    if os.path.exists(path):
          if os.path.isdir(path):
                data = "Yes the path exist . Its a folder"
          else :
                data = "Yes the path exist . Its a file"
    else :
            data = "Path does not exist"
    return data

@mcp.tool()       
def specific_entry_lister(type:str,path:str):
        "Lists only the files or only the folders (not both) directly inside a given directory, one level deep — does not look inside subfolders."
        try :
                    checking_path_exist(path)
                    with open((path,"specific_entry.txt"),"w+") as f:
                            file = None
                            folder = None
                            if type == "file":
                                    file = True
                            else :
                                    folder = True
                            items = os.listdir(path)
                            for item in items :
                                       full_path = os.path.join(path,item)
                                       check = os.path.isdir(full_path)
                                       if check and folder:
                                                f.write(f"\n{item}")
                                       elif not check and file :
                                                f.write(f"\n{item}")
                            data = f.read
        except Exception as e:
                  data =  f"error occured . error : {e}"

        return data

@mcp.tool()
def specific_entry_adder(path:str,type:str,name:str,file_type:str):
        "Creates a new empty file or a new empty folder at the given path. For files, only plain text-based formats are allowed (e.g. txt, md, py)."
        data = None
        file_type_list = ["txt", "md", "log", "csv", "env", "yaml", "yml", "py", "sh", "html"]
        try :
                       if type == "file":
                                      if file_type.lower() not in file_type_list:
                                              raise ValueError("The file type you mentioned is invalid . check is it a text based format or it contains dot")
                                      with open(os.path.join(path,f"{name}.{file_type.lower()}"),"w") as f:
                                              pass
                       elif type == "folder":
                                      full_path = os.path.join(path,name)
                                      os.mkdir(full_path)
                       data = f"{type} creation status : Done"
        except Exception as e :
                       data =   f"{type} creation failed due to error : {e}"
        return data


def checking_the_safety_of_data(path):
        safe_root = "/home/coder/Videos"
        if path.startswith(safe_root):
                 pass
        else :
                raise ValueError("The path is invalid . you dont have permission to acces this")


@mcp.tool()
def entry_remover(path:str) :
        "Permanently deletes a file, or a folder and everything inside it (including all nested subfolders and files), at the given path. Only paths inside the allowed safe directory can be deleted; requests outside that area will be rejected"
        data = None
        try :
            checking_path_exist(path)
            checking_the_safety_of_data(path)
            if os.path.isdir(path):
                             os.rmdir(path)
                             data = "Folder deletion status : Done"
            else :
                             os.remove(path)
                             data = "File deletion status : Done"
        except Exception as e:
                  data = f"Deletion status Failed due to error : {e}"
        return data

if __name__ == "__main__":
        mcp.run()