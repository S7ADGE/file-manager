from pathlib import Path
import hashlib

def choose_action():

    print("\nWhat would you like to do?\n")
    print("\t1. Display the files and folders in the specified path")
    print("\t2. Find and delete duplicate files")
    print("\t3. Do both")

    choise = input("\nEnter your choice (1, 2, or 3) : ").replace(" ", "")

    while choise not in ["1", "2", "3"]:

        print("\t\nInvalid choice! Please choose 1, 2, or 3.")
        choise = input("\nEnter your choice (1, 2, or 3) : ").replace(" ", "")

    return choise

def action():

    choise = choose_action()

    if choise == "3":

        show()
        same_size()

    else:

        if choise == "1":

            show()

        else:

            same_size()

def show():

    print("\n==================================== SHOW ====================================")
    print("\nDiratories : \n")

    for item in folder.iterdir():

        if item.is_dir():

            print("\t", item.name)

    print("\n", "-" * 77, "\n")
    print("Files : ")

    for item in folder.iterdir():

        if item.is_file():

            print("\t", item.name)


def size():
    
    files_by_size = {}

    for item in folder.iterdir():

        if item.is_file():

            if item.stat().st_size in files_by_size:

                files_by_size[item.stat().st_size].append(item.name)

            else:

                files_by_size[item.stat().st_size] = [item.name]

    return files_by_size

def same_size():

    duplicate_files = size()
    print("\n========================== Potential Duplicates(size) ==========================\n")
    
    for files in duplicate_files.values():

        if len(files) > 1:

            print(files)

path = input("Enter the folder path : ")
folder = Path(path).expanduser()

while folder.exists() == False:

    print("Folder is not exist")
    path = input("Enter the folder path : ")
    folder = Path(path).expanduser()

action()
