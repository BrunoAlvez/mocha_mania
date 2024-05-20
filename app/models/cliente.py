from datetime import datetime

from app.models.fidelidade import Fidelidade
from app.models.pessoa import Pessoa


class Cliente(Pessoa):
    def __init__(
            self,
            id: int,
            nome: str,
            login: str,
            email: str,
            senha: str,
            cpf: str,
            data_de_nascimento: datetime,
            telefone: str,
    ):
        super().__init__(
            id=id,
            nome=nome,
            login=login,
            email=email,
            senha=senha,
            cpf=cpf,
            data_de_nascimento=data_de_nascimento,
            telefone=telefone,
        )
        self.__cpf = cpf
        self.__data_de_nascimento = data_de_nascimento
        self.__telefone = telefone
        self.__fidelidade = None

    @staticmethod
    def escondidos() -> list:
        return ['senha']

    def validacoes(self) -> dict:
        validacoes = super().validacoes()
        validacoes['validacoes'].update({
            'cpf': ['required', 'string', 'cpf'],
            'data_de_nascimento': ['required', 'date'],
            'telefone': ['required', 'string', 'telefone'],
            'fidelidade': ['nullable', 'instance:Fidelidade'],
        })
        validacoes['traducoes'].update({
            'cpf': 'CPF',
            'data_de_nascimento': 'data de nascimento',
        })
        return validacoes

    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def data_de_nascimento(self) -> datetime:
        return self.__data_de_nascimento

    @property
    def telefone(self) -> str:
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str):
        self.__telefone = telefone

    @property
    def fidelidade(self) -> Fidelidade or None:
        return self.__fidelidade

    @fidelidade.setter
    def fidelidade(self, fidelidade: Fidelidade):
        self.__fidelidade = fidelidade
