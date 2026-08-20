from mcp.server import MCPServer
import os

mcp = MCPServer("file helper tools")

def checking_path_exist(path):
        if os.path.exists(path):
                pass
        else :
                raise ValueError("Path doesnt exist")

@mcp.tool()
def content_fetcher(path,depth=0):
    "Recursively lists all files and subfolders inside a given directory, including everything nested at any depth, and returns the result in an indented tree structure showing the folder hierarchy"
    data = None
    try:
                      checking_path_exist(path)
                      with open(f"{path}\Content_tree.txt","w+") as f:
                              items  = os.listdir(path)
                              for item in items :
                                     full_path = os.path.join(path,item)
                                     indent = "     "*depth

                                     if os.path.isdir(full_path):
                                               f.write(f"\n{indent} {item}")
                                               content_fetcher(full_path,depth+1)
                                     else :
                                                f.write(f"\n{indent} {item}")
                              text = f.read()
                              data = text
    except Exception as e :
            data = f"error occured . error : {e}"

    return data 

@mcp.tool()
def specific_entry_exist_checker(path):
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
def specific_entry_lister(type,path):
        "Lists only the files or only the folders (not both) directly inside a given directory, one level deep — does not look inside subfolders."
        try :
                    checking_path_exist(path)
                    with open(f"{path}\specific_entry.txt","w+") as f:
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
def specific_entry_adder(path,type,name,file_type):
        "Creates a new empty file or a new empty folder at the given path. For files, only plain text-based formats are allowed (e.g. txt, md, py)."
        data = None
        file_type_list = ["txt", "md", "log", "csv", "env", "yaml", "yml", "py", "sh", "html"]
        try :
                       if type == "file":
                                      if file_type.lower() not in file_type_list:
                                              raise ValueError("The file type you mentioned is invalid . check is it a text based format or it contains dot")
                                      with open(f"{path}/{name}.{file_type.lower()}","w") as f:
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
def entry_remover(path) :
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