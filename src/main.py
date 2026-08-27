from pathlib import Path
import hashlib

def choose_action():

    print("\nWhat would you like to do?\n")
    print("\t1. Display the files and folders in the specified path")
    print("\t2. Find duplicate files")
    print("\t3. Do both")

    choise = input("\nEnter your choice (1, 2, or 3) : ").replace(" ", "")

    while choise not in ["1", "2", "3"]:

        print("\t\nInvalid choice! Please choose 1, 2, or 3.")
        choise = input("\nEnter your choice (1, 2, or 3) : ").replace(" ", "")

    return choise

def action():

    choise = choose_action()
    print("\n==================================== SHOW ====================================")

    if choise == "3":

        show_content()
        show_duplicate()

    else:

        if choise == "1":

            show_content()

        else:

            show_duplicate()

def show_content():

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

                files_by_size[item.stat().st_size].append(item)

            else:

                files_by_size[item.stat().st_size] = [item]

    return files_by_size

def same_size():

    duplicate_files = size()
    same_list = []
    
    for files in duplicate_files.values():

        if len(files) > 1:

            same_list.append(files)

    return same_list

def same_hash():

    size_list = same_size()
    hash_dic = {}
    
    for group in size_list:

        for item in group:

            hash_object = hashlib.sha256()
    
            with open(item, "rb") as file:

                while chunk := file.read(4096):

                    hash_object.update(chunk)

                hash_dic[item] = hash_object.hexdigest()

    return hash_dic

def duplicate():

    same = same_hash()
    hash_list = []
    duplicate_list = []

    for key, value in same.items():

        if value in hash_list:

            duplicate_list.append(key.name)

        hash_list.append(value)

    return duplicate_list

def show_duplicate():

    duplicate_file = duplicate()
    print("\n", "-" * 77, "\n")
    print("Duplicate Files : \n")

    if duplicate_file == []:

        print("No duplicate files were found in this path.")

    for file in duplicate_file:

        print("\t", file)

path = input("Enter the folder path : ")
folder = Path(path).expanduser()

while folder.exists() == False:

    print("Folder is not exist")
    path = input("Enter the folder path : ")
    folder = Path(path).expanduser()

action()
