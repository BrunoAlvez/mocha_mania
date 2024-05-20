def input_int(mensagem: str = '', minimo: int = None, maximo: int = None) -> int:
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f'O valor deve ser maior ou igual a {minimo}!')
            elif maximo is not None and valor > maximo:
                print(f'O valor deve ser menor ou igual a {maximo}!')
            else:
                return valor
        except ValueError:
            print('Por favor, digite um número inteiro válido!')

