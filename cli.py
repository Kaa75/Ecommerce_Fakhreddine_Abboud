import os
import subprocess

from tap import Tap

SEP = os.path.sep


class ArgumentParser(Tap):
    command: str
    tests: bool = True
    fixtures: bool = False

    def configure(self) -> None:
        self.add_argument("command", type=str, help="Command to run")
        self.add_argument("--tests", type=bool, help="Generate test files")
        self.add_argument(
            "--fixtures", type=bool, help="Generate fixtures for test files"
        )


def run() -> None:
    """
    command: run
    Run the fastapi backend server
    """
    subprocess.run(["uvicorn", "src.main:app", "--reload"])


def clean(files: list[str] = ["src", "tests", "cli.py"]) -> None:
    """
    command: clean
    Clean up the code
    """
    subprocess.run(
        [
            "autoflake",
            "-r",
            "--exclude=__init__.py, conftest.py",
            "--remove-all-unused-imports",
            "--remove-unused-variables",
            "-i",
            *files,
        ]
    )
    subprocess.run(["isort", *files, "--profile", "black"])
    subprocess.run(["black", *files])
    subprocess.run(["mypy", "--strict", *files])


def generate_test_files(tests: bool = True, fixtures: bool = False) -> None:
    """
    command: generate-test-files
    Generate empty test files in the `tests` and `tests/fixtures`
    directories for all the files in the `src` directory.
    """
    src_dir = "src"
    test_dir = "tests"
    fixtures_dir = f"tests{SEP}fixtures"
    for dirpath, dirnames, filenames in os.walk(src_dir):
        if "__pycache__" in dirpath:
            continue
        relative_path = os.path.relpath(dirpath, src_dir)
        test_path = os.path.join(test_dir, relative_path)
        fixtures_path = os.path.join(fixtures_dir, relative_path)

        if tests:
            os.makedirs(test_path, exist_ok=True)
            init_file = os.path.join(test_path, "__init__.py")
            open(init_file, "w").close()

        if fixtures:
            os.makedirs(fixtures_path, exist_ok=True)
            init_file = os.path.join(fixtures_path, "__init__.py")
            open(init_file, "w").close()

        for filename in filenames:
            if filename.endswith(".py"):
                if filename == "__init__.py":
                    continue
                test_filename = "test_" + filename
                if tests:
                    test_file = os.path.join(test_path, test_filename)
                    open(test_file, "a").close()

                if fixtures:
                    fixture_file = os.path.join(fixtures_path, filename)
                    open(fixture_file, "a").close()


def import_fixtures() -> None:
    """
    command: import-fixtures
    This command imports all the fixtures in the
    `tests/fixtures` directory to the `conftest.py` file.
    """
    conftest = open(f"tests{SEP}conftest.py", "w")
    fixtures = os.path.join("tests", "fixtures")
    for dirpath, dirnames, filenames in os.walk(fixtures):
        for filename in filenames:
            if filename.endswith(".py"):
                lines = open(os.path.join(dirpath, filename)).read().split("\n")
                i = 0
                function_names = []
                while i < len(lines):
                    line = lines[i]
                    if "@pytest.fixture" == line[:15]:
                        line = lines[i + 1]
                        function_names.append(line.split("def ")[1].split("(")[0])
                    i += 1
                if function_names:
                    path = os.path.relpath(dirpath, fixtures).replace(SEP, ".")
                    path = f".fixtures.{path}.{filename.split('.')[0]}"
                    while ".." in path:
                        path = path.replace("..", ".")
                    conftest.write(f"from {path} import {', '.join(function_names)}\n")
    conftest.close()
    clean(["tests/conftest.py"])


def run_tests() -> None:
    """
    command: run-tests
    This command runs all the tests in the `tests` directory.
    """
    subprocess.run(["pytest", "tests"])


def clean_unused_files() -> None:
    """
    command: clean-unused-files
    This command deletes all the test files in the `tests` and `tests/fixtures` directories that empty.
    This command also deletes the test files in the `tests` directory that do not have a corresponding file in the `src` directory.
    """
    # ! Refactor this code; it is not working as expected
    # ! This command does not work recursively for some reason
    # TODO: Fix this code
    for dirpath, dirnames, filenames in os.walk("tests"):
        if "__pycache__" in dirpath:
            continue
        if "fixtures" in dirpath:
            continue
        if "conftest.py" in filenames:
            filenames.remove("conftest.py")
        for filename in filenames:
            if filename.endswith(".py"):
                if filename == "__init__.py":
                    continue
                file = os.path.join(dirpath, filename)
                file = file.replace("test_", "")
                file = file.replace("tests", "src")
                if not os.path.exists(file):
                    os.remove(os.path.join(dirpath, filename))
                    print(f"Deleted {os.path.join(dirpath, filename)}")
    for dirpath, dirnames, filenames in os.walk("tests/fixtures"):
        if "__pycache__" in dirpath:
            continue
        if "others" in dirpath:
            continue
        for filename in filenames:
            if filename.endswith(".py"):
                if file.endswith("__init__.py"):
                    continue
                file = os.path.join(dirpath, filename)
                file = file.replace("tests/fixtures", "src")
                if not os.path.exists(file):
                    os.remove(os.path.join(dirpath, filename))
                file = os.path.join(dirpath, filename)
                if not open(file).read().strip():
                    os.remove(file)
                    print(f"Deleted {file}")


def pre_stage() -> None:
    """
    command: pre-stage
    This command runs the `import-fixtures`,
    `clean` and `run-tests` commands in this order.
    """
    import_fixtures()
    clean()
    run_tests()


def help() -> None:
    """
    command: help
    Show help
    """
    print("Usage: python cli.py [command]")
    print("Commands:")
    commands: list[dict[str, str]] = []
    for name, obj in globals().items():
        if obj.__class__.__name__ == "type":
            continue
        if callable(obj):
            if type(obj.__doc__) != str:
                continue
            commands.append(
                {
                    "command": obj.__doc__.split("\n")[1].split(":")[1].strip(),
                    "description": "\n".join(obj.__doc__.split("\n")[2:-1]),
                }
            )
    max_command_length = max([len(command["command"]) for command in commands])
    for cmd in commands:
        command = cmd["command"]
        description = cmd["description"]
        desc_lines = description.split("\n")
        print(f"\t{command:<{max_command_length}}:\t{desc_lines[0]}")
        for line in desc_lines[1:]:
            print(f"\t{'':<{max_command_length}} \t{line}")
        print()


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    args = arg_parser.parse_args()

    if args.command == "clean":
        clean()
    elif args.command == "run":
        run()
    elif args.command == "generate-test-files":
        generate_test_files(
            tests=args.tests,
            fixtures=args.fixtures,
        )
    elif args.command == "import-fixtures":
        import_fixtures()
    elif args.command == "run-tests":
        run_tests()
    elif args.command == "pre-stage":
        pre_stage()
    elif args.command == "clean-unused-files":
        clean_unused_files()
    elif args.command == "help":
        help()
    else:
        print("Invalid command")
        help()
        exit(1)
