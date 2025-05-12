import argparse

import pyperclip

from py_project_mapper.models import PythonFile
from py_project_mapper.utils import walk_python_files


def main():
    parser = argparse.ArgumentParser(description="Analyze Python project structure.")
    parser.add_argument("-p", "--project_path", required=True, help="The path to the project directory.")
    parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help="Copy the formatted output to the clipboard."
    )
    args = parser.parse_args()

    output_accumulator = [] # To store all formatted strings

    for file_path in walk_python_files(args.project_path):
        file = PythonFile(file_path)
        formatted_file_output = file.formatted()
        output_accumulator.append(formatted_file_output)

    full_output = "\n\n".join(output_accumulator)

    if args.copy:
        try:
            pyperclip.copy(full_output)
        except pyperclip.PyperclipException as e:
            print(f"\n--- Could not copy to clipboard: {e} ---")
            print(full_output)
    else:
        print(full_output)


if __name__ == "__main__":
    main()
