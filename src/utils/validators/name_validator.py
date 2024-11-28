"""Module for validating user names."""

def validate_name(v: str) -> str:
    """
    Validate a user's full name.

    Args:
        v (str): The full name to validate.

    Returns:
        str: The validated name.

    Raises:
        ValueError: If the name does not contain first and last name,
                    contains non-alphabetic characters,
                    or does not start with a capital letter.
    """
    try:
        first_name, last_name = v.split(" ")
        if not first_name.isalpha() and not last_name.isalpha():
            raise ValueError("Name must only contain characters")
        if not first_name[0].isupper() and not last_name[0].isupper():
            raise ValueError("Name must start with a capital letter")
        return v
    except ValueError:
        raise ValueError("Name must contain a first and last name")
