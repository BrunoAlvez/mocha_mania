import re


def camel_to_snake(string: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def camel_to_pascal(string: str) -> str:
    return string[0].upper() + string[1:]


def snake_to_camel(string: str) -> str:
    pascal = snake_to_pascal(string)
    return pascal_to_camel(pascal)


def snake_to_pascal(string: str) -> str:
    return ''.join(word.title() for word in string.split('_'))


def pascal_to_camel(string: str) -> str:
    return string[0].lower() + string[1:]


def pascal_to_snake(string: str) -> str:
    return camel_to_snake(string)
