from pathlib import Path

def get_path():

    path = input("Enter the folder path : ")
    folder = Path(path).expanduser()

    while folder.exists() == False:

        print("Folder is not exist")
        path = input("Enter the folder path : ")
        folder = Path(path).expanduser()

    return folder

def show():

    folder = get_path()

    print("\nDiratories : \n")

    for item in folder.iterdir():

        if item.is_dir():

            print("\t", item.name)

    print("\n", "-" * 47, "\n")
    print("Files : ")

    for item in folder.iterdir():

        if item.is_file():

            print("\t", item.name )

show()

