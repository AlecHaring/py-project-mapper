# py-project-mapper

py-project-mapper is a command-line tool that analyzes and displays the structure of Python projects. It scans the specified directory to find all Python files and extracts information about variables, functions, classes, and their relationships.

## Features

- Recursively scans a specified directory to find all Python files
- Parses each Python file and extracts information about:
  - Variables
  - Functions and their signatures
  - Classes, their base classes, and their methods
- **Optional clipboard support** – add `-c / --copy` to copy the formatted output directly to your clipboard  


## Installation

```bash
pip install git+https://github.com/AlecHaring/py-project-mapper.git
```


## Usage

To analyze a Python project and display its structure, run the following command:
```bash
py-project-mapper -p /path/to/project/directory

py-project-mapper -p /path/to/project/directory -c   # analyze and copy the result to clipboard
```

Replace `/path/to/project/directory` with the path to the Python project you want to analyze.

## Example Output
```
File: /path/to/project/directory/main.py
 Variables:
 - variable1
 - variable2
 Functions:
        def function1(arg1: int, arg2: str) -> None
 Classes:
        class ClassName(BaseClass)
            def method1(arg1: float) -> List[str]
```


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
