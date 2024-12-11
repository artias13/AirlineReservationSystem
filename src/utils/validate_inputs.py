import re

def validate_non_empty_string(value, field_name):
    """
    Validates that a string is not empty.

    Args:
        value (str): The string to validate.
        field_name (str): The name of the field being validated.

    Returns:
        str: The stripped string if valid.

    Raises:
        ValueError: If the string is empty after stripping.
    """
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty")
    return value.strip()

def validate_positive_integer(value, field_name):
    """
    Validates that a value is a positive integer.

    Args:
        value (str): The value to validate.
        field_name (str): The name of the field being validated.

    Returns:
        int: The parsed positive integer.

    Raises:
        ValueError: If the value is not a valid positive integer.
    """
    try:
        num = int(value)
        if num <= 0:
            raise ValueError(f"{field_name} must be a positive integer")
        return num
    except ValueError:
        raise ValueError(f"{field_name} must be a valid integer")

def validate_email(email):
    """
    Validates an email address format.

    Args:
        email (str): The email address to validate.

    Returns:
        str: The email address if valid.

    Raises:
        ValueError: If the email format is invalid.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    return email

def validate_password(password):
    """
    Validates a password length.

    Args:
        password (str): The password to validate.

    Returns:
        str: The password if valid.

    Raises:
        ValueError: If the password length is less than 8 characters.
    """
    if len(password) < 4:
        raise ValueError("Password must be at least 8 characters long")
    return password

def validate_phone_number(phone_number):
    """
    Validates a phone number format.

    Args:
        phone_number (str): The phone number to validate.

    Returns:
        str: The phone number if valid.

    Raises:
        ValueError: If the phone number format is invalid.
    """
    pattern = r'[\+\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
    if not re.match(pattern, phone_number):
        raise ValueError("Invalid phone number format")
    return phone_number