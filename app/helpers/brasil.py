import re


def validar_cpf(cpf: str) -> bool:
    cpf = cpf.replace('.', '').replace('-', '')
    if len(cpf) != 11:
        return False

    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    if resto < 2:
        penultimo_digito = 0
    else:
        penultimo_digito = 11 - resto

    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    if resto < 2:
        ultimo_digito = 0
    else:
        ultimo_digito = 11 - resto

    return penultimo_digito == int(cpf[9]) and ultimo_digito == int(cpf[10])


def validar_telefone(telefone: str) -> bool:
    return re.match(r'^\(\d{2}\) \d{4,5}-\d{4}$', telefone) is not None
