from app.enums.cargo_enum import CargoEnum
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
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

    def cadastrar(self, dados: dict) -> Funcionario:
        erros = []
        for funcionario_registrado in self.__funcionarios:
            if funcionario_registrado.email == dados['email']:
                erros.append({'email': 'Email já cadastrado'})
            if funcionario_registrado.login == dados['login']:
                erros.append({'login': 'Login já cadastrado'})
        if len(erros) > 0:
            raise RegraDeNegocioException('Email ou login já cadastrado', {
                'erros': erros,
            })
        funcionario = Funcionario(**dados)
        self.__funcionarios.append(funcionario)
        return funcionario

    def atualizar(self, funcionario: Funcionario, dados: dict) -> Funcionario:
        for atributo, valor in dados.items():
            if atributo == 'cargo':
                if valor == 1:
                    valor = CargoEnum.ATENDENTE.value
                elif valor == 2:
                    valor = CargoEnum.BARISTA.value
            setattr(funcionario, atributo, valor)
        return funcionario

    def remover(self, id: int):
        funcionario_removido = self.encontrar(id)
        self.__funcionarios.remove(funcionario_removido)

    def encontrar(self, id: int) -> Funcionario or None:
        for funcionario in self.__funcionarios:
            if funcionario.id == id:
                return funcionario
        raise Exception('Funcionário não encontrado')

    def listar(self) -> [Funcionario]:
        return self.__funcionarios

    def validar_usuario(self, login: str, senha: str) -> Funcionario or None:
        for funcionario in self.__funcionarios:
            if (funcionario.email == login or funcionario.login == login) and funcionario.senha == senha:
                return funcionario
        return None
