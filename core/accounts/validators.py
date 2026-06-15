import re

def validate_iranian_phone(phone):
    pattern = r'^(?:\+98|0098|0)?9\d{9}$'
    return bool(re.match(pattern, phone))