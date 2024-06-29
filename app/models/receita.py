from app.enums.unidade_tempo_enum import UnidadeTempoEnum
from app.models.model_base import ModelBase


class Receita(ModelBase):
    def __init__(self, nome: str, preparos: list):
        super().__init__(nome=nome, preparos=preparos)
        self.__nome = nome
        self.__preparos = preparos

    @staticmethod
    def all() -> list:
        return Receita.persistencia().buscar()

    @staticmethod
    def find(id: int) -> 'Receita':
        return Receita.persistencia().visualizar(id)

    def validacoes(self) -> dict:
        return {
            'validacoes': {
                'nome': ['required', 'string'],
                'preparos': ['required', 'list', 'instance:Preparo'],
            },
            'traducoes': {
                'id': 'ID',
            }
        }

    @staticmethod
    def persistencia():
        from database.persistencias.receita_persistencia import ReceitaPersistencia
        return ReceitaPersistencia()

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def preparos(self) -> list:
        return self.__preparos

    def tempo_preparo(self) -> dict:
        tempo = 0
        for preparo in self.__preparos:
            if preparo.tempo is None:
                continue

            if preparo.unidade_tempo == UnidadeTempoEnum.SEGUNDO:
                tempo += preparo.tempo
            elif preparo.unidade_tempo == UnidadeTempoEnum.MINUTO:
                tempo += preparo.tempo * 60
            elif preparo.unidade_tempo == UnidadeTempoEnum.HORA:
                tempo += preparo.tempo * 3600

        if tempo < 60:
            return {'tempo': tempo, 'unidade': UnidadeTempoEnum.SEGUNDO}
        elif tempo < 3600:
            return {'tempo': tempo / 60, 'unidade': UnidadeTempoEnum.MINUTO}
        return {'tempo': tempo / 3600, 'unidade': UnidadeTempoEnum.HORA}
