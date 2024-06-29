from app.enums.cargo_enum import CargoEnum
from app.models.funcionario import Funcionario
from app.services.item_service import ItemService
from app.services.pedido_service import PedidoService
from app.services.service_base import ServiceBase
from database.seeders.funcionario_gerente_seeder import FuncionarioGerenteSeeder


class FuncionarioService(ServiceBase):
    def __init__(self, item_service: ItemService, pedido_service: PedidoService):
        self.__funcionarios = FuncionarioGerenteSeeder().run()
        self.__item_service = item_service
        self.__pedido_service = pedido_service

    @property
    def funcionarios(self) -> [Funcionario]:
        return self.__funcionarios

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
