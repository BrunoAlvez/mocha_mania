from app.enums.cargo_enum import CargoEnum
from app.models.pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(
            self,
            nome: str,
            login: str,
            email: str,
            senha: str,
            cargo: CargoEnum,
    ):
        super().__init__(nome, login, email, senha)
        self.__cargo = cargo

    def validacoes(self) -> dict:
        validacoes = super().validacoes()
        validacoes['validacoes'].update({
            'cargo': ['required', 'string', 'enum:CargoEnum'],
        })
        return validacoes

    @staticmethod
    def persistencia():
        from database.persistencias.funcionario_persistencia import FuncionarioPersistencia
        return FuncionarioPersistencia()

    @staticmethod
    def all() -> list:
        return Funcionario.persistencia().buscar()

    @staticmethod
    def find(id: int) -> 'Funcionario':
        return Funcionario.persistencia().visualizar(id)

    @property
    def cargo(self) -> CargoEnum:
        return self.__cargo

    @cargo.setter
    def cargo(self, cargo: CargoEnum):
        self.__cargo = cargo
