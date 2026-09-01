from pathlib import Path
import hashlib


def get_valid_input(prompt: str, valid_choices: list[str]):
    """Prompt the user until they enter a value that exists in the allowed answer list."""

    choice = input(prompt).lower().strip()

    # Keep asking until the input matches one of the allowed answers
    while choice not in valid_choices:
        
        print(f"\n\tInvalid selection. Please choose an item from the {valid_choices}") 

        choice = input(prompt).lower().strip()

    return choice


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


def show_content(folder: Path):
    """Print all folders and files found directly inside the given folder."""

    dirs = [item for item in folder.iterdir() if item.is_dir()]
    files = [item for item in folder.iterdir() if item.is_file()]

    print("\nFolder(s) :\n")

    if dirs:

        for item in dirs:

            print("\t", item.name)
    else:

        print("\tNo folders found in the specified path.")

    print("\n", "-" * 77, "\n")
    print("File(s) :\n")

    if files:

        for item in files:

            print("\t", item.name)

    else:

        print("\tNo files found in the specified path.")


def hash_file(path: Path, chunk_size: int = 4096) -> str:
    """Return the SHA-256 hash of a file's contents."""

    hasher = hashlib.sha256()

    # Read the file in chunks for better memory efficiency with large files
    with open(path, "rb") as f:

        while chunk := f.read(chunk_size):

            hasher.update(chunk)

    return hasher.hexdigest()


def find_duplicates(folder: Path):
    """Find duplicate files in the given folder and return them as a list of Path objects.

    Duplicates are detected in two passes for efficiency:
    1. Group files by size, since files with different sizes can't be duplicates.
    2. Hash only the files that share a size with at least one other file,
       then group by hash to confirm which ones are true duplicates.
    The first file in each duplicate group is kept; the rest are returned.
    """

    # Step 1: group files by size
    file_by_size = {}

    for item in folder.iterdir():

        if item.is_file():

            file_size = item.stat().st_size

            # If this size has already been seen, append the file to its list
            if file_size in file_by_size:

                file_by_size[file_size].append(item)

            # Otherwise, create a new list for this size
            else:

                file_by_size[file_size] = [item]

    # Step 2: hash only files that share a size with at least one other file
    file_by_hash = {}

    for same_size_files in file_by_size.values():

        if len(same_size_files) > 1:

            for file in same_size_files:

                file_hash = hash_file(file)

                # If this hash has already been seen, group it with the matching file(s)
                if file_hash in file_by_hash:

                    file_by_hash[file_hash].append(file)

                # Otherwise, create a new list for this hash
                else:

                    file_by_hash[file_hash] = [file]

    # Step 3: any hash with more than one file means real duplicates,
    # keep the first copy and mark the rest as duplicates
    final_duplicates = []

    for files in file_by_hash.values():

        if len(files) > 1:

            final_duplicates.extend(files[1:])

    return final_duplicates


def show_duplicates(duplicates: list[Path]):
    """Print the list of duplicate files."""

    print("\nDuplicate File(s) :\n")

    if not duplicates:

        print("\tNo duplicate files found.")

        return

    for file in duplicates:

        print("\t", file.name)


def delete_files(files: list[Path]):
    """Ask the user for confirmation, then delete the duplicate files if confirmed."""

    print("\n=================================== DELETE ===================================")
    choice = get_valid_input("\nDo yo want to delete the duplicate file(s)? (y/N) : ", ["y", "n"])

    if choice == "y":

        # Remove every duplicate file found earlier
        for file in files:

            file.unlink()

        print("\n\t\t Duplicate file(s) deleted successfully ! ")

    else:

        print("\n\t\tDeletion cancelled. No file(s) have been deleted !")


def run(folder: Path):
    """Prompt the user to select a menu option, then run the corresponding action(s)."""
    
    print("\nWhat would you like to do?\n")
    print("\t1. Display the files and folders in the specified path")
    print("\t2. Find and delete duplicate files")
    print("\t3. Do both")

    choice = get_valid_input("\nEnter your choice (1, 2, or 3) : ", ["1", "2", "3"])

    print("\n==================================== SHOW ====================================")

    # Show folder/file listing for choices 1 and 3
    if choice in ("1", "3"):

        show_content(folder)

        if choice == "3":

            print("\n", "-" * 77)

    # Find, show, and optionally delete duplicates for choices 2 and 3
    if choice in ("2", "3"):

        duplicates = find_duplicates(folder)

        show_duplicates(duplicates)

        if duplicates:

            delete_files(duplicates)


def main():
    """Entry point: get a valid folder from the user, then run the program."""

    folder = get_valid_folder()
    run(folder)


if __name__ == "__main__":

    main()
