from mcp.server import MCPServer
from typing import Annotated
from pydantic import Field
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
def making_absolute_path(
        path:Annotated[str,Field(description="The raw path or location exactly as the user described it, in any form — relative, partial, or absolute. Do not attempt to correct, clean, or guess the proper format yourself; pass it as-is and this tool will resolve it correctly.")]
        ):
        "Converts any path or location description into a correct, complete absolute path. This tool must be called first, before any other tool that takes a path argument (content_fetcher, specific_entry_lister, specific_entry_adder, entry_remover, specific_entry_exist_checker). Pass whatever location the user described, in whatever form they gave it — this tool handles resolving it correctly. Use the exact result this tool returns as the path argument for the next tool call."
        BASE_DIR = "/home/coder"
        if os.path.isabs(path):
                real_path = path
        else :
                real_path = os.path.join(BASE_DIR,path)
        return os.path.normpath(real_path)

@mcp.tool()
def entry_remover(
        path: Annotated[str,Field(description="The full path of the file or folder to permanently delete. Deleting a folder also deletes everything inside it, including nested subfolders and files. Only paths within an allowed safe directory can be deleted — paths outside it will be rejected and nothing will be deleted.")]
        ) :
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


@mcp.tool()
def content_fetcher(
        path: Annotated[str,Field(description="The full path of the directory to scan. Returns every file and subfolder nested inside, at any depth, including hidden folders like .git — this can produce a very large result for folders containing version control repositories or many nested files. For a simple, one-level listing instead, use specific_entry_lister.")]
        ):
    "Recursively lists all files and subfolders inside the given directory path, including everything nested at any depth, and returns the result as an indented tree structure showing the folder hierarchy. Takes a single argument: the folder path to start from."
    data = None
    try:
                      checking_path_exist(path)
                      path_for_content_fetcher = "/home/coder"
                      full_path_content_tree = os.path.join(path_for_content_fetcher,"Content_tree.txt")
                      with open(full_path_content_tree,"w+") as f :
                              function_for_content_fetcher(path,f)
                              f.seek(0)
                              text = f.read()
                              data = text
                      entry_remover(full_path_content_tree)
    except Exception as e :
            data = f"error occured . error : {e}"

    return data 


@mcp.tool()
def specific_entry_exist_checker(
        path:Annotated[str,Field(description="The full path to check for existence.")]
        ):
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
def specific_entry_lister(
        type: Annotated[str,Field(description="Must be exactly 'file' to list only files, or 'folder' to list only folders. No other values are valid.")],
        path: Annotated[str,Field(description="The folder path to list content from.")]
                          ):
        "Lists only the files or only the folders (not both) directly inside a given directory, one level deep — does not look inside subfolders."
        try :
                    checking_path_exist(path)
                    path_for_specific_entry = "/home/coder"
                    full_path_specific_entry = os.path.join(path_for_specific_entry,"specific_entry.txt")
                    with open(full_path_specific_entry,"w+") as f:
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
                            f.seek(0)
                            data = f.read()
                    entry_remover(full_path_specific_entry)
        except Exception as e:
                  data =  f"error occured . error : {e}"

        return data

@mcp.tool()
def specific_entry_adder(
        path: Annotated[str,Field(description="The directory where the new file or folder should be created. This should be the parent location only — do not include the new file or folder's name in this path; provide that separately.")],
        type: Annotated[str,Field(description="Must be exactly 'file' or 'folder'. Use 'file' to create a new file. Use 'folder' to create a new folder ")],
        name : Annotated[str,Field(description="The base file name only, without any extension (e.g. 'notes', not 'notes.txt') — the extension is provided separately via the file_type parameter.")],
        file_type : Annotated[str,Field(description="The file extension to use, without a leading dot (e.g. 'txt', not '.txt'). Must be a text-based format: one of txt, md, log, csv, env, yaml, yml, py, sh, html. Other formats will be rejected.")]
                          ):
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



if __name__ == "__main__":
        mcp.run()