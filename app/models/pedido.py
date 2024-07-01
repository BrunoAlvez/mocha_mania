from datetime import datetime

from app.enums.status_pedido_enum import StatusPedidoEnum
from app.models.cliente import Cliente
from app.models.model_base import ModelBase


class Pedido(ModelBase):
    def __init__(self, cliente: Cliente, itens: list, responsavel=None, status=StatusPedidoEnum.PENDENTE):
        super().__init__(cliente=cliente, itens=itens, responsavel=responsavel, status=status)
        self.__data = datetime.now()
        self.__status = status
        self.__itens = itens
        self.__cliente = cliente
        self.__responsavel = responsavel

    def validacoes(self) -> dict:
        return {
            'validacoes': {
                'data': ['required', 'date'],
                'status': ['required', 'enum:StatusPedidoEnum'],
                'itens': ['required', 'list', 'min:1', 'instance:Produto,Ingrediente'],
                'cliente': ['required', 'instance:Cliente'],
                'responsavel': ['nullable', 'instance:Funcionario'],
            },
            'traducoes': {
                'id': 'ID',
                'responsavel': 'responsável',
            }
        }

    @staticmethod
    def persistencia():
        from database.persistencias.pedido_persistencia import PedidoPersistencia
        return PedidoPersistencia()

    @staticmethod
    def all() -> list:
        return Pedido.persistencia().buscar()

    @staticmethod
    def find(id: int) -> 'Pedido':
        return Pedido.persistencia().visualizar(id)

    @property
    def data(self) -> datetime:
        return self.__data

    @property
    def status(self) -> StatusPedidoEnum:
        return self.__status

    @status.setter
    def status(self, status: StatusPedidoEnum):
        self.__status = status

    @property
    def itens(self) -> list:
        return self.__itens

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def responsavel(self):
        return self.__responsavel

    @responsavel.setter
    def responsavel(self, responsavel):
        self.__responsavel = responsavel

    def to_dict(self) -> dict:
        dados = super().to_dict()

        valor_total = 0
        itens_agrupados = {}
        for item in self.__itens:
            if item.id not in itens_agrupados:
                itens_agrupados[item.id] = {
                    'item': item,
                    'quantidade': 0,
                }
            itens_agrupados[item.id]['quantidade'] += 1

        for item in itens_agrupados.values():
            valor_total += item['item'].preco * item['quantidade']
        dados['valor'] = valor_total
        return dados
