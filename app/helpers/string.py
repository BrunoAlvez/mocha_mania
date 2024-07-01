import re
from datetime import datetime


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


def mascara_telefone(telefone: str) -> str:
    if len(telefone) > 15:
        return telefone[:15]

    com_regex = re.sub(r'\D', '', telefone)
    if len(com_regex) == 0:
        formatado = ''
    elif len(com_regex) <= 2:
        formatado = '({}'.format(com_regex)
    elif len(com_regex) <= 6:
        formatado = '({}) {}'.format(com_regex[:2], com_regex[2:])
    elif len(com_regex) <= 10:
        formatado = '({}) {}-{}'.format(com_regex[:2], com_regex[2:6], com_regex[6:])
    else:
        formatado = '({}) {}-{}'.format(com_regex[:2], com_regex[2:7], com_regex[7:])
    return formatado


def mascara_cpf(cpf: str) -> str:
    if len(cpf) > 14:
        return cpf[:14]

    com_regex = re.sub(r'\D', '', cpf)
    if len(com_regex) == 0:
        formatado = ''
    elif len(com_regex) <= 3:
        formatado = '{}'.format(com_regex)
    elif len(com_regex) <= 6:
        formatado = '{}.{}'.format(com_regex[:3], com_regex[3:])
    elif len(com_regex) <= 9:
        formatado = '{}.{}.{}'.format(com_regex[:3], com_regex[3:6], com_regex[6:])
    else:
        formatado = '{}.{}.{}-{}'.format(com_regex[:3], com_regex[3:6], com_regex[6:9], com_regex[9:])
    return formatado


def mascara_data(data: str) -> str:
    if len(data) > 10:
        return data[:10]

    com_regex = re.sub(r'\D', '', data)
    if len(com_regex) == 0:
        formatado = ''
    elif len(com_regex) <= 2:
        formatado = '{}'.format(com_regex)
    elif len(com_regex) <= 4:
        formatado = '{}/{}'.format(com_regex[:2], com_regex[2:])
    else:
        formatado = '{}/{}/{}'.format(com_regex[:2], com_regex[2:4], com_regex[4:])
    return formatado


def replace_last(string: str, old: str, new: str) -> str:
    return string[::-1].replace(old[::-1], new[::-1], 1)[::-1]


def formatar_preco(preco: float) -> str:
    return f'R${preco:.2f}'.replace('.', ',')


def formatar_data(data: datetime, com_hora=False) -> str:
    if com_hora:
        return data.strftime('%d/%m/%Y %H:%M:%S')
    return data.strftime('%d/%m/%Y')
