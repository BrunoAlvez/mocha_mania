from app.exceptions.sair_exception import SairException
from app.helpers.input import input_int


class ViewBase:
    def _input_int_com_sair(self, mensagem: str = '', minimo: int = None, maximo: int = None) -> int:
        valor = input_int(mensagem, minimo, maximo)
        if valor == 0:
            raise SairException
        erro = False
        if minimo is not None and valor < minimo:
            print(f'O valor deve ser maior ou igual a {minimo}!')
            erro = True
        if maximo is not None and valor > maximo:
            print(f'O valor deve ser menor ou igual a {maximo}!')
            erro = True
        if erro:
            return self._input_int_com_sair(mensagem, minimo, maximo)
        return valor

    def _input_str_com_sair(self, mensagem: str = '', minimo: int = None, maximo: int = None) -> str:
        valor = input(mensagem)
        if valor == '0':
            raise SairException
        erro = False
        if maximo is not None and len(valor) > maximo:
            print(f'O valor deve ter no máximo {maximo} caracteres!')
            erro = True
        if minimo is not None and len(valor) < minimo:
            print(f'O valor deve ter no mínimo {minimo} caracteres!')
            erro = True
        if erro:
            return self._input_str_com_sair(mensagem, minimo, maximo)
        return valor

    @staticmethod
    def sair() -> int:
        print('Tem certeza que deseja sair?')
        return input_int('[1] - Sim [2] - Não\n', 1, 2)
