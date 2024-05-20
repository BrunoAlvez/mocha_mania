from app.enums.cargo_enum import CargoEnum
from app.models.pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(
            self,
            id: int,
            nome: str,
            login: str,
            email: str,
            senha: str,
            cargo: CargoEnum,
    ):
        super().__init__(id, nome, login, email, senha)
        self.__cargo = cargo

    def validacoes(self) -> dict:
        validacoes = super().validacoes()
        validacoes['validacoes'].update({
            'cargo': ['required', 'string', 'enum:CargoEnum'],
        })
        return validacoes

    @property
    def cargo(self) -> CargoEnum:
        return self.__cargo

    @cargo.setter
    def cargo(self, cargo: CargoEnum):
        self.__cargo = cargo
