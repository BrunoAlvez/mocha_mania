from app.enums.unidade_enum import UnidadeEnum
from app.models.item import Item


class Produto(Item):
    def __init__(self,
                 id: int,
                 nome: str,
                 quantidade: float,
                 descricao: str,
                 preco: float,
                 preparos: list = [],
                 ):
        super().__init__(id, nome, quantidade, UnidadeEnum.UNIDADE)
        self.__id = id
        self.__nome = nome
        self.__descricao = descricao
        self.__preco = preco
        self.__preparos = preparos

    def validacoes(self) -> dict:
        validacoes = super().validacoes()
        validacoes['validacoes'].update({
            'descricao': ['required', 'string', 'min:5', 'max:255'],
            'preco': ['required', 'float'],
        })
        validacoes['traducoes'].update({
            'descricao': 'Descrição',
            'preco': 'Preço',
        })
        return validacoes

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, preco: float):
        self.__preco = preco

    @property
    def preparos(self) -> list:
        return self.__preparos

    def preparado(self) -> bool:
        return len(self.__preparos) > 0
