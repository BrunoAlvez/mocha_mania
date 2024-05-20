from abc import abstractmethod

from app.enums.unidade_enum import UnidadeEnum
from app.models.model_base import ModelBase


class Item(ModelBase):
    @abstractmethod
    def __init__(self, id: int, nome: str, quantidade: float, unidade: UnidadeEnum):
        self.__id = id
        self.__nome = nome
        self.__quantidade = quantidade
        self.__unidade = unidade

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def quantidade(self) -> float:
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade: float):
        self.__quantidade = quantidade

    @property
    def unidade(self) -> UnidadeEnum:
        return self.__unidade

    @unidade.setter
    def unidade(self, unidade: UnidadeEnum):
        self.__unidade = unidade

    @staticmethod
    def validacoes() -> dict:
        return {
            'validacoes': {
                'id': ['required', 'integer'],
                'nome': ['required', 'string'],
                'quantidade': ['nullable', 'numeric'],
                'unidade': ['required', 'string', 'enum:UnidadeEnum'],
            },
            'traducoes': {
                'id': 'ID',
            }
        }
