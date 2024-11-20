def validate_name(v: str) -> str:
    if not v.isalpha():
        raise ValueError("Name must only contain characters")
    if not v.strip():
        raise ValueError("Name cannot be empty")
    if not v[0].isupper():
        raise ValueError("Name must start with a capital letter")
    return v
