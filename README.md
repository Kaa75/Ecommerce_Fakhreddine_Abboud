# Ecommerce API Backend

A simple GPA calculator that allows students to calculate their GPA based on their grades and credit hours.

## Setup the environment

1. Install Python 3.12 or higher
2. Create a virtual environment

```bash
python -m venv .venv
```

3. Activate the virtual environment

```bash
source .venv/bin/activate # For macos
.venv\Scripts\activate # For windows
```

4. Install the required packages

```bash
pip install -r requirements.txt
```

## Some Commands

### Run backend server

Run the fastapi backend server

```bash
python cli.py run
```

### Clean the code (necessary before creating a pull request)

Clean up the code

```bash
python cli.py clean
```

### Generate empty test files

Generate empty test files in the `tests` and `tests/fixtures` directories for all the files in the `src` directory.

```bash
python cli.py generate-test-files
```

### Import fixtures to `conftest.py`

This command imports all the fixtures in the `tests/fixtures` directory to the `conftest.py` file.

```bash
python cli.py import-fixtures
```

### Run tests

This command runs all the tests in the `tests` directory.

```bash
python cli.py run-tests
```

### Clean unused tests and fixtures

This command deletes all the test files in the `tests` and `tests/fixtures` directories that empty.

```bash
python cli.py clean-unused-tests
```

### Run pre-stage command

This command runs the `import-fixtures`, `clean` and `run-tests` commands in this order.

```bash
python cli.py pre-stage
```

## Contributors

- [Karim Abboud](https://github.com/Kaa75)
- [Rayan Fakhreddine](https://github.com/Rayan28461)
