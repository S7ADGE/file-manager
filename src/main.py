import duplicate_finder as df
from pathlib import Path


def get_valid_folder():
    """Prompt the user until they enter a folder path that actually exists."""

    path = input("Enter the folder path : ")
    folder = Path(path).expanduser()

    # Keep asking until a valid folder path is provided
    while not folder.exists():

        print("Folder is not exist")
        path = input("Enter the folder path : ")
        folder = Path(path).expanduser()

    return folder


def run(folder: Path):
    """Prompt the user to select a menu option, then run the corresponding action(s) from duplicate_finder."""
    
    print("\nWhat would you like to do?\n")
    print("\t1. Display the files and folders in the specified path")
    print("\t2. Find and delete duplicate files")
    print("\t3. Do both")

    choice = df.get_valid_input("\nEnter your choice (1, 2, or 3) : ", ["1", "2", "3"])

    print("\n==================================== SHOW ====================================")

    # Show folder/file listing for choices 1 and 3
    if choice in ("1", "3"):

        df.show_content(folder)

        if choice == "3":

            print("\n", "-" * 77)

    # Find, show, and optionally delete duplicates for choices 2 and 3
    if choice in ("2", "3"):

        duplicates = df.find_duplicates(folder)

        df.show_duplicates(duplicates)

        if duplicates:

            df.delete_files(duplicates)


def main():
    """Entry point: get a valid folder from the user, then run the program."""

    folder = get_valid_folder()
    run(folder)


if __name__ == "__main__":

    main()
