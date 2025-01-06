import argparse
import logging
import os
import sys
import zipfile

DEFAULT_INCLUDES = ['.py', '.json', '.yaml']
DEFAULT_EXCLUDES = ['venv', '__pycache__', '.git', '.idea']


def add_to_zip(zipf, directory, includes, excludes):
    for root, dirs, files in os.walk(directory):
        if any(exclude in root for exclude in excludes):
            dirs.clear()
            continue
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file_path)[1]
            if file_ext in includes:
                logging.info(f"Adding: {file_path}")
                zipf.write(file_path, os.path.relpath(file_path, directory))
            else:
                logging.debug(f"Skipping: {file_path}")


def main():
    parser = argparse.ArgumentParser(description="Create a zip archive of selected files and folders.")
    parser.add_argument("path", help="Path to the directory to zip.")
    parser.add_argument("--log", choices=["info", "debug"], default="info", help="Log level: info or debug.")
    parser.add_argument("--excludes", nargs="*", default=DEFAULT_EXCLUDES, help="Folders to exclude.")
    parser.add_argument("--includes", nargs="*", default=DEFAULT_INCLUDES, help="File extensions to include.")
    parser.add_argument('-a', "--add-includes", nargs="*", default=[], help="Additional file extensions to include.")
    parser.add_argument('-e', "--add-excludes", nargs="*", default=[], help="Additional folder to exclude.")
    parser.add_argument("--output", default="archive.zip", help="Name of the output zip archive.")
    args = parser.parse_args()

    includes = set(args.includes + args.add_includes)
    excludes = set(args.excludes + args.add_excludes)

    print("Includes", includes)
    print("Excludes", excludes)
    print("Path", os.path.abspath(args.path))
    input("Press [Enter] to continue. ")

    log_level = logging.DEBUG if args.log == "debug" else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

    with zipfile.ZipFile(args.output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        add_to_zip(zipf, args.path, includes, excludes)

    print(f"Zip file '{args.output}' created successfully.")


if __name__ == "__main__":
    main()
