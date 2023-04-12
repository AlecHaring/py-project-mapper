import argparse

from py_project_mapper.utils import walk_python_files, parse_python_file, print_python_structure


def main():
    parser = argparse.ArgumentParser(description="Analyze Python project structure.")
    parser.add_argument("-p", "--project_path", required=True, help="The path to the project directory.")
    args = parser.parse_args()

    for file_path in walk_python_files(args.project_path):
        file_data = parse_python_file(file_path)
        print_python_structure(file_data)
        print("\n")


if __name__ == "__main__":
    main()
