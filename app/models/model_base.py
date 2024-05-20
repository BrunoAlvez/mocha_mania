from abc import abstractmethod, ABC

import app.helpers.regras as regras


class ModelBase(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        self.__valida_dados(**kwargs)

    def __setattr__(self, atributo, value):
        self.__valida_dados(**{atributo: value})
        super().__setattr__(atributo, value)

    def to_dict(self) -> dict:
        modelo_dict = {}
        for atributo, valor in self.__dict__.items():
            atributo = atributo.split('__')[-1]

            if atributo in self.escondidos():
                continue

            if isinstance(valor, ModelBase):
                modelo_dict[atributo] = valor.to_dict()
            else:
                modelo_dict[atributo] = valor
        return modelo_dict

    @staticmethod
    def escondidos() -> list:
        return []

    @staticmethod
    @abstractmethod
    def validacoes() -> dict:
        pass

    def __valida_dados(self, **valores):
        if not hasattr(self, 'validacoes'):
            return

        if 'validacoes' not in self.validacoes():
            validacoes: dict = {}
        else:
            validacoes: dict = self.validacoes()['validacoes']

        if 'traducoes' not in self.validacoes():
            traducoes: dict = {}
        else:
            traducoes: dict = self.validacoes()['traducoes']
        regras.validar(valores, validacoes, traducoes)