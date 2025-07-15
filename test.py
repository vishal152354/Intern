from pathlib import Path
import os
def check_folder(folder_path):
    folder = Path(folder_path)

    if folder.is_dir():
        return next(folder.iterdir())
    else :
        return False


def number_of_files(folder_path):
    count = 0 
    try:
        for folder_path, _, files in os.walk(folder_path):
            count += len(files)
    except FileNotFoundError:
        print("file not found")
    except Exception as e :
        print("error",e)

a = check_folder(r"C:\Users\50054\Desktop\intern-Vishal\data")
if a==0 :
    print("folder empty")
else:
    print ("folder non-empty")

n = number_of_files(r"c:\Users\50054\Desktop\intern-Vishal\data")
print("number of files",n)