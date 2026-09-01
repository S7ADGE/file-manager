# file-manager

A simple command-line tool written in Python to explore a folder's contents and find (and optionally delete) duplicate files based on their SHA-256 hash.

## Features

- 📂 **List contents** — display all folders and files directly inside a given path
- 🔍 **Find duplicates** — detect duplicate files by comparing file size first, then SHA-256 hash for accuracy
- 🗑️ **Delete duplicates** — remove duplicate files after an explicit confirmation prompt
- ⚡ **Efficient** — only hashes files that already share a size with another file, avoiding unnecessary I/O on large folders

## How it works

Duplicate detection runs in two passes:

1. **Group by size** — files are grouped by their size in bytes. Files with a unique size can't have duplicates, so they're skipped.
2. **Group by hash** — only files that share a size with at least one other file are hashed (SHA-256, read in 4KB chunks for memory efficiency). Files with a matching hash are true duplicates.

For each group of duplicates found, the first copy is kept and the rest are flagged for deletion.

## Requirements

- Python 3.9+ (uses the `list[Path]` built-in generic type hint syntax)
- No external dependencies — uses only the standard library (`pathlib`, `hashlib`)

## Usage

Clone the repository and run the script:

```bash
git clone https://github.com/S7ADGE/file-manager.git
cd file-manager
python file_manager.py
```

You'll be prompted for a folder path, then asked what you'd like to do:

```
Enter the folder path : /path/to/folder

What would you like to do?

    1. Display the files and folders in the specified path
    2. Find and delete duplicate files
    3. Do both

Enter your choice (1, 2, or 3) :
```

### Option 1 — Display contents

Lists all subfolders and files found directly inside the given path.

### Option 2 — Find and delete duplicates

Scans the folder for duplicate files and prints the ones found. If any are found, you'll be asked to confirm before they're permanently deleted:

```
Do you want to delete the duplicate file(s)? (y/n) :
```

⚠️ **Deletion is permanent.** Files are removed with `Path.unlink()`, which does not send them to the recycle bin / trash. Review the list carefully before confirming.

### Option 3 — Do both

Runs the display and duplicate-detection steps one after another.

## Project structure

```
file-manager/
├── file_manager.py   # main script
└── README.md
```

| Function | Purpose |
|---|---|
| `get_valid_input()` | Reprompt until the user enters an allowed choice |
| `get_valid_folder()` | Reprompt until the user enters a path that exists |
| `show_content()` | Print folders and files in the given directory |
| `hash_file()` | Compute the SHA-256 hash of a file |
| `find_duplicates()` | Return duplicate files using the size → hash strategy |
| `show_duplicates()` | Print the list of duplicate files found |
| `delete_files()` | Confirm with the user, then delete the given files |
| `run()` | Handle the menu and dispatch to the right action(s) |
| `main()` | Entry point |

## Notes / limitations

- Only scans the **top level** of the given folder — it does not recurse into subfolders.
- Duplicate detection is content-based (via hash), not name-based — files with different names but identical content are still detected.

## License

No license specified yet — add a `LICENSE` file if you'd like to define usage terms for this project.
