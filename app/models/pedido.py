from datetime import datetime

from app.enums.status_pedido_enum import StatusPedidoEnum
from app.models.cliente import Cliente
from app.models.model_base import ModelBase


class Pedido(ModelBase):
    def __init__(self, id: int, cliente: Cliente, itens: list):
        super().__init__()
        self.__id = id
        self.__data = datetime.now()
        self.__status = StatusPedidoEnum.PENDENTE
        self.__itens = itens
        self.__cliente = cliente
        self.__responsavel = None

    @staticmethod
    def validacoes() -> dict:
        return {
            'validacoes': {
                'id': ['required', 'integer'],
                'data': ['required', 'date'],
                'status': ['required', 'enum:StatusPedidoEnum'],
                'itens': ['required', 'list', 'min:1', 'instance:Produto'],
                'cliente': ['required', 'instance:Cliente'],
                'responsavel': ['nullable', 'instance:Funcionario'],
            },
            'traducoes': {
                'id': 'ID',
                'responsavel': 'responsável',
            }
        }

    @property
    def id(self) -> int:
        return self.__id

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
        for item in self.__itens:
            valor_total += item.preco * item.quantidade

        dados['valor'] = valor_total
        return dados
