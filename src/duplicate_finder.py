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
    choice = get_valid_input("\nDo you want to delete the duplicate file(s)? (y/N) : ", ["y", "n"])

    if choice == "y":

        # Remove every duplicate file found earlier
        for file in files:

            file.unlink()

        print("\n\t\t Duplicate file(s) deleted successfully ! ")

    else:

        print("\n\t\tDeletion cancelled. No file(s) have been deleted !")
