from abc import abstractmethod

from app.models.model_base import ModelBase


class Pessoa(ModelBase):
    @abstractmethod
    def __init__(self, id: int, nome: str, login: str, email: str, senha: str, **kwargs):
        super().__init__(id=id, nome=nome, login=login, email=email, senha=senha, **kwargs)
        self.__id = id
        self.__nome = nome
        self.__login = login
        self.__email = email
        self.__senha = senha

    @staticmethod
    def validacoes() -> dict:
        return {
            'validacoes': {
                'id': ['required', 'integer'],
                'nome': ['required', 'string', 'min:5', 'max:100'],
                'login': ['required', 'string', 'min:5', 'max:50'],
                'email': ['required', 'string', 'email'],
                'senha': ['required', 'string', 'min:8', 'max:50']
            },
            'traducoes': {
                'id': 'ID',
                'email': 'e-mail',
            }
        }

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
    def login(self) -> str:
        return self.__login

    @login.setter
    def login(self, login: str):
        self.__login = login

    @property
    def email(self) -> str:
        return self.__email

    @property
    def senha(self) -> str:
        return self.__senha

    @senha.setter
    def senha(self, senha: str):
        self.__senha = senha
