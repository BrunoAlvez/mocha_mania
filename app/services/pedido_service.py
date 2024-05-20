from datetime import datetime

from app.enums.status_pedido_enum import StatusPedidoEnum
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.models.funcionario import Funcionario
from app.models.pedido import Pedido
from app.services.item_service import ItemService
from app.services.service_base import ServiceBase


class PedidoService(ServiceBase):
    def __init__(self, item_service: ItemService):
        self.__item_service = item_service
        self.__pedidos = []

    @property
    def pedidos(self):
        return self.__pedidos

    def cadastrar(self, dados: dict):
        pedido = Pedido(**dados)
        self.__pedidos.append(pedido)
        return pedido

    def atualizar(self, pedido: Pedido, dados: dict):
        pass

    def remover(self, id: int):
        raise RegraDeNegocioException('Não é possível remover um pedido')

    def encontrar(self, id: int) -> Pedido:
        for pedido in self.__pedidos:
            if pedido.id == id:
                return pedido
        raise Exception('Pedido não encontrado')

    def listar(self, filtros: dict = None) -> list:
        pedidos = self.__pedidos
        if filtros is not None:
            if 'cliente_id' in filtros:
                pedidos = list(filter(lambda pedido: pedido.cliente.id == filtros['cliente_id'], pedidos))
            if 'status' in filtros:
                pedidos = list(filter(lambda pedido: pedido.status == filtros['status'], pedidos))
            if 'data' in filtros:
                pedidos = list(filter(lambda pedido: pedido.data.date() == filtros['data'].date(), pedidos))
        return pedidos

    def assumir(self, id: int, funcionario: Funcionario) -> Pedido:
        pedido = self.encontrar(id)
        pedido.responsavel = funcionario
        pedido.status = StatusPedidoEnum.EM_PREPARO
        return pedido

    def finalizar(self, id: int) -> Pedido:
        pedido = self.encontrar(id)
        pedido.status = StatusPedidoEnum.FINALIZADO
        return pedido
