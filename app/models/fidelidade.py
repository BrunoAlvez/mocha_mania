from app.enums.classificacao_penalidade_enum import ClassificacaoPenalidadeEnum
from app.models.model_base import ModelBase


class Fidelidade(ModelBase):
    def __init__(self):
        self.__pontos: int = 0
        self.__classificacao: str = ClassificacaoPenalidadeEnum.BRONZE.value

    def validacoes(self) -> dict:
        return {
            'validacoes': {
                'pontos': ['required', 'integer'],
                'classificacao': ['required', 'string', 'enum:ClassificacaoPenalidadeEnum'],
            },
            'traducoes': {
                'classificacao': 'classificação',
            },
        }

    @staticmethod
    def persistencia():
        from database.persistencias.fidelidade_persistencia import FidelidadePersistencia
        return FidelidadePersistencia()

    @staticmethod
    def all() -> list:
        return Fidelidade.persistencia().buscar()

    @staticmethod
    def find(id: int) -> 'Fidelidade':
        return Fidelidade.persistencia().visualizar(id)

    @property
    def pontos(self) -> int:
        return self.__pontos

    @pontos.setter
    def pontos(self, pontos: int):
        self.__pontos = pontos

        pontos_das_classificacoes = {
            ClassificacaoPenalidadeEnum.DIAMANTE.value: ClassificacaoPenalidadeEnum.DIAMANTE.minimo_de_pontos(),
            ClassificacaoPenalidadeEnum.OURO.value: ClassificacaoPenalidadeEnum.OURO.minimo_de_pontos(),
            ClassificacaoPenalidadeEnum.PRATA.value: ClassificacaoPenalidadeEnum.PRATA.minimo_de_pontos(),
            ClassificacaoPenalidadeEnum.BRONZE.value: ClassificacaoPenalidadeEnum.BRONZE.minimo_de_pontos(),
        }

        for classificacao, minimo_de_pontos in pontos_das_classificacoes.items():
            if pontos >= minimo_de_pontos:
                self.classificacao = classificacao
                break

    @property
    def classificacao(self) -> str:
        return self.__classificacao

    @classificacao.setter
    def classificacao(self, classificacao: str):
        self.__classificacao = classificacao
