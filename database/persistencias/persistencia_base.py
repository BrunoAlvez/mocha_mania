from abc import ABC, abstractmethod
import pickle
from typing import Type

from app.models.model_base import ModelBase
import app.helpers.string as string_helper


class PersistenciaBase(ABC):
    @abstractmethod
    def __init__(self, modelo: Type[ModelBase], datasource: str = None):
        self.__modelo = modelo
        self.__datasource = self.__datasource(modelo, datasource)
        self.__cache = {}
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    @staticmethod
    def __datasource(modelo: Type[ModelBase], datasource: str = None) -> str:
        if datasource is not None:
            nome_datasource = datasource
        else:
            nome_datasource = string_helper.pascal_to_snake(modelo.__name__).replace('_', 's_') + 's'
        return f'database/pkls/{nome_datasource}.pkl'

    def __id(self) -> int:
        cache_ids = {}
        try:
            cache_ids = pickle.load(open('database/pkls/sequels.pkl', 'rb'))
            ultimo_id_modelo = cache_ids[self.__datasource]
            id_atual = ultimo_id_modelo + 1
        except FileNotFoundError:
            cache_ids = {}
            id_atual = 1
        except KeyError:
            id_atual = 1
        cache_ids[self.__datasource] = id_atual
        pickle.dump(cache_ids, open('database/pkls/sequels.pkl', 'wb'))
        return id_atual

    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, 'wb'))

    def __load(self):
        self.__cache = pickle.load(open(self.__datasource, 'rb'))

    def buscar(self) -> list:
        return list(self.__cache.values())

    def cadastrar(self, modelo: ModelBase) -> ModelBase:
        self.__validar_instancia(modelo)

        id = self.__id()
        modelo.id = id
        self.__cache[id] = modelo
        self.__dump()
        return modelo

    def visualizar(self, id: int) -> ModelBase or None:
        return self.__cache.get(id)

    def atualizar(self, modelo: ModelBase) -> ModelBase:
        self.__validar_instancia(modelo)

        id = modelo.__getattribute__('id')
        modelo.id = id
        self.__cache[id] = modelo
        self.__dump()
        return modelo

    def remover(self, id: int):
        try:
            self.__cache.pop(id)
        except KeyError:
            raise ValueError(f'O objeto com ID #{id} não foi encontrado!')
        self.__dump()

    def __validar_instancia(self, modelo: ModelBase):
        if not isinstance(modelo, self.__modelo):
            raise ValueError(f'O objeto passado não é uma instância de {self.__modelo}!')
