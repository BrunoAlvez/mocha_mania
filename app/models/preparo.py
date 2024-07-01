from app.enums.unidade_enum import UnidadeEnum
from app.enums.unidade_tempo_enum import UnidadeTempoEnum
from app.models.ingrediente import Ingrediente
from app.models.model_base import ModelBase


class Preparo(ModelBase):
    def __init__(
            self,
            ingrediente: Ingrediente,
            quantidade: float,
            unidade: UnidadeEnum,
            descricao: str,
            tempo: float or None,
            unidade_tempo: UnidadeTempoEnum or None,
    ):
        super().__init__(
            ingrediente=ingrediente,
            quantidade=quantidade,
            unidade=unidade,
            descricao=descricao,
            tempo=tempo,
            unidade_tempo=unidade_tempo,
        )
        self.__ingrediente = ingrediente
        self.__quantidade = quantidade
        self.__unidade = unidade
        self.__descricao = descricao
        self.__tempo = tempo
        self.__unidade_tempo = unidade_tempo

    def validacoes(self) -> dict:
        return {
            'validacoes': {
                'ingrediente': ['required', 'instance:Ingrediente'],
                'quantidade': ['required', 'float'],
                'unidade': ['required', 'string', 'enum:UnidadeEnum'],
                'descricao': ['required', 'string'],
                'tempo': ['nullable', 'float'],
                'unidade_tempo': ['nullable', 'string', 'enum:UnidadeTempoEnum'],
            },
            'traducoes': {
                'descricao': 'descrição',
                'unidade_tempo': 'unidade de tempo',
            }
        }

    @staticmethod
    def persistencia():
        from database.persistencias.preparo_persistencia import PreparoPersistencia
        return PreparoPersistencia()

    @staticmethod
    def all() -> list:
        return Preparo.persistencia().buscar()

    @staticmethod
    def find(id: int) -> 'Preparo':
        return Preparo.persistencia().visualizar(id)

    @property
    def ingrediente(self) -> Ingrediente:
        return self.__ingrediente

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
    def unidade(self, unidade: str):
        self.__unidade = unidade

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def tempo(self) -> float or None:
        return self.__tempo

    @tempo.setter
    def tempo(self, tempo: float):
        self.__tempo = tempo

    @property
    def unidade_tempo(self) -> str or None:
        return self.__unidade_tempo

    @unidade_tempo.setter
    def unidade_tempo(self, unidade_tempo: str):
        self.__unidade_tempo = unidade_tempo
