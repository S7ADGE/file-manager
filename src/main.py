from pathlib import Path
import hashlib


def ans(prompt, answer=["y", "n"]):
    """Prompt the user until they enter a value that exists in the allowed answer list."""

    ans = input(prompt).lower().replace(" ", "")

    # Keep asking until the input matches one of the allowed answers
    while ans not in answer:
        
        print(f"\n\tInvalid selection. Please choose an item from the {answer}")
        ans = input(prompt).lower().replace(" ", "")

    return ans


def choose_action():
    """Prompt the user to select a menu option and return the validated choice."""

    print("\nWhat would you like to do?\n")
    print("\t1. Display the files and folders in the specified path")
    print("\t2. Find duplicate files")
    print("\t3. Do both")
    choise = ans("\nEnter your choice (1, 2, or 3) : ", ["1", "2", "3"])

    return choise


def action():
    """Run the appropriate function(s) based on the user's menu choice."""

    choise = choose_action()
    print("\n==================================== SHOW ====================================")

    if choise == "3":
        # Run both operations
        show_content()
        print("\n", "-" * 77)
        show_duplicate()

    else:

        if choise == "1":
            # Only show folder contents
            show_content()

        else:
            # Only show duplicate files
            show_duplicate()


def show_content():
    """Print the names of all folders and files found in the given path."""

    print("\nDiratories : \n")

    # Print directory names
    for item in folder.iterdir():

        if item.is_dir():

            print("\t", item.name)

    print("\n", "-" * 77, "\n")
    print("Files : ")

    # Print file names
    for item in folder.iterdir():

        if item.is_file():

            print("\t", item.name)


def size():
    """Group files by their size and return a dict of {size: [files]}."""
    
    files_by_size = {}

    for item in folder.iterdir():

        if item.is_file():

            # If this size has already been seen, append the file to its list
            if item.stat().st_size in files_by_size:

                files_by_size[item.stat().st_size].append(item)

            # Otherwise, create a new list for this size
            else:

                files_by_size[item.stat().st_size] = [item]

    return files_by_size


def same_size():
    """Return only the groups of files that share the same size (duplicate candidates)."""

    duplicate_files = size()
    same_list = []
    
    for files in duplicate_files.values():

        # More than one file with the same size means they might be duplicates
        if len(files) > 1:

            same_list.append(files)

    return same_list


def same_hash():
    """Compute the SHA-256 hash for same-size files and return a dict of {file: hash}."""

    size_list = same_size()
    hash_dic = {}
    
    for group in size_list:

        for item in group:

            hash_object = hashlib.sha256()
    
            # Read the file in chunks for better memory efficiency with large files
            with open(item, "rb") as file:

                while chunk := file.read(4096):

                    hash_object.update(chunk)

                hash_dic[item] = hash_object.hexdigest()

    return hash_dic


# Module-level list holding the duplicate files found across calls to duplicate()
duplicate_list = []


def duplicate():
    """Compare file hashes and return a list of names of truly duplicate files."""

    same = same_hash()
    hash_list = []
    
    for key, value in same.items():

        # If this hash has already been seen, the file is a duplicate
        if value in hash_list:

            duplicate_list.append(key.name)

        hash_list.append(value)

    return duplicate_list


def show_duplicate():
    """Print the list of duplicate files found."""

    duplicate_file = duplicate()
    print("\nDuplicate Files : \n")
    duplicate_file_del = []

    if duplicate_file == []:

        print("\tNo duplicate files were found in this path!")

    else:

        for file in duplicate_file:

            print("\t", file)

# ---- Main program execution ----

path = input("Enter the folder path : ")
folder = Path(path).expanduser()

# Keep asking until a valid folder path is provided
while folder.exists() == False:

    print("Folder is not exist")
    path = input("Enter the folder path : ")
    folder = Path(path).expanduser()

action()