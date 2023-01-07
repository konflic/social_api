def validator_password(password: str) -> str:
    if password != None:
        special_characters = "[~\!@#\$%\^&\*\(\)_\+\":;'\[\]]}{"
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least 1 digit.")
        if not any(char.isalpha() for char in password):
            raise ValueError("Password must contain at least 1 letter.")
        if not any(char in special_characters for char in password):
            raise ValueError("Password must contain at least 1 special character.")
    return password


def validator_name(name: str) -> str:
    if name is not None:
        special_characters = "[~\!@#\$%\^&\*\(\)_\+\":;'\[\]]}{"
        if any(char.isdigit() for char in name):
            raise ValueError("A name cannot contain numbers.")
        if any(char in special_characters for char in name):
            raise ValueError("A name can not contain a special character.")
    return name
