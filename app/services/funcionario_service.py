from app.enums.cargo_enum import CargoEnum
from app.models.funcionario import Funcionario
from app.services.service_base import ServiceBase


class FuncionarioService(ServiceBase):
    @staticmethod
    def cadastrar(dados: dict) -> Funcionario:
        return Funcionario(**dados).create()

    @staticmethod
    def atualizar(funcionario: Funcionario, dados: dict) -> Funcionario:
        for atributo, valor in dados.items():
            if atributo == 'cargo':
                if valor == 1:
                    valor = CargoEnum.ATENDENTE.value
                elif valor == 2:
                    valor = CargoEnum.BARISTA.value
            setattr(funcionario, atributo, valor)
        return funcionario

    @staticmethod
    def remover(id: int):
        Funcionario.delete(Funcionario.find(id))

    @staticmethod
    def encontrar(id: int) -> Funcionario or None:
        return Funcionario.find(id)

    @staticmethod
    def listar(filtros: dict = None) -> [Funcionario]:
        return Funcionario.all()

    @staticmethod
    def validar_usuario(login: str, senha: str) -> Funcionario or None:
        for funcionario in Funcionario.all():
            if (funcionario.email == login or funcionario.login == login) and funcionario.senha == senha:
                return funcionario
        return None
