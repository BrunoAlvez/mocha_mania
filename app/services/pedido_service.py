from datetime import datetime

from app.enums.status_pedido_enum import StatusPedidoEnum
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.models.funcionario import Funcionario
from app.models.pedido import Pedido
from app.services.item_service import ItemService
from app.services.service_base import ServiceBase


class PedidoService(ServiceBase):
    @staticmethod
    def pedidos():
        return Pedido.all()

    @staticmethod
    def cadastrar(dados: dict) -> Pedido:
        return Pedido(**dados).create()

    @staticmethod
    def atualizar(pedido: Pedido, dados: dict):
        raise RegraDeNegocioException('Não é possível atualizar um pedido')

    @staticmethod
    def remover(id: int):
        raise RegraDeNegocioException('Não é possível remover um pedido')

    @staticmethod
    def encontrar(id: int) -> Pedido:
        return Pedido.find(id)

    @staticmethod
    def listar(filtros: dict = None) -> list:
        pedidos = Pedido.all()
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
