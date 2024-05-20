def is_int(valor) -> bool:
    return isinstance(valor, int) or (isinstance(valor, str) and valor.isdigit())


def is_float(valor) -> bool:
    return (isinstance(valor, float)
            or (isinstance(valor, str) and valor.replace('.', '', 1).isdigit()))
