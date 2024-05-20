from app.controllers.controller_base import ControllerBase
from app.enums.status_pedido_enum import StatusPedidoEnum
from app.models.funcionario import Funcionario
from app.services.pedido_service import PedidoService
from app.views.pedido_view import PedidoView


class PedidoController(ControllerBase):
    def __init__(self, pedido_service: PedidoService):
        self._view = PedidoView()
        self.__pedidos = []
        self.__service = pedido_service
        self.__usuario_logado = None
        self.__ao_sair = None

    @property
    def usuario_logado(self) -> Funcionario:
        return self.__usuario_logado

    @usuario_logado.setter
    def usuario_logado(self, usuario: Funcionario):
        self.__usuario_logado = usuario

    @property
    def ao_sair(self) -> callable:
        return self.__ao_sair

    @ao_sair.setter
    def ao_sair(self, ao_sair: callable):
        self.__ao_sair = ao_sair

    @property
    def pedidos(self):
        return self.__pedidos

    def menu(self):
        opcao = self._view.menu()
        if opcao == 1:
            self.__listar()
        elif opcao == 0:
            self.__ao_sair()
        else:
            self.menu()

    def __listar(self):
        pedidos = self.__service.listar()
        pedidos_repositorio = []
        for pedido in pedidos:
            pedidos_repositorio.append(self._repositorio(pedido))
        opcao = self._view.listar(pedidos_repositorio)
        if opcao == 0:
            self.menu()
        else:
            self.__encontrar(opcao)

    def __encontrar(self, id: int):
        pedido = self.__service.encontrar(id)
        pedido_repositorio = self._repositorio(pedido)
        opcao = self._view.detalhes(pedido_repositorio)
        if opcao == 1 and pedido.status == StatusPedidoEnum.PENDENTE:
            self.__assumir(id)
        elif opcao == 0:
            self.menu()
        else:
            self.__encontrar(id)

    def __assumir(self, id: int):
        self.__service.assumir(id, self.__usuario_logado)
        finalizado = self._view.assumir()
        if finalizado:
            self.__service.finalizar(id)
            self.menu()
        else:
            self.__assumir(id)

    def sem_pedidos(self):
        self._view.sem_pedidos()
