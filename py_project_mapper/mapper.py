import argparse

from py_project_mapper.models import PythonFile
from py_project_mapper.utils import walk_python_files


def main():
    parser = argparse.ArgumentParser(description="Analyze Python project structure.")
    parser.add_argument("-p", "--project_path", required=True, help="The path to the project directory.")
    args = parser.parse_args()

    for file_path in walk_python_files(args.project_path):
        file = PythonFile(file_path)
        print(file.formatted())


if __name__ == "__main__":
    main()
