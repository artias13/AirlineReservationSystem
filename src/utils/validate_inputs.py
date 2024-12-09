import re

def validate_non_empty_string(value, field_name):
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty")
    return value.strip()

def validate_positive_integer(value, field_name):
    try:
        num = int(value)
        if num <= 0:
            raise ValueError(f"{field_name} must be a positive integer")
        return num
    except ValueError:
        raise ValueError(f"{field_name} must be a valid integer")

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    return email

def validate_password(password):
    if len(password) < 4:
        raise ValueError("Password must be at least 8 characters long")
    return password

def validate_phone_number(phone_number):
    pattern = r'[\+\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
    if not re.match(pattern, phone_number):
        raise ValueError("Invalid phone number format")
    return phone_number