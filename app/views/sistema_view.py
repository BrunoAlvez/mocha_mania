from copy import copy

from app.helpers.input import input_int
from app.views.view_base import ViewBase


class SistemaView(ViewBase):
    def __init__(self):
        pass

    @staticmethod
    def menu() -> int:
        print('###         Bem-vindo ao MochaMania!         ###')
        print('### O aplicativo número 1 em vendas de café! ###')
        print()
        print('Escolha uma opção:')
        print('[1] Login - [2] Quero me cadastrar - [0] Sair')
        return input_int('Digite a opção desejada: ')

    def login(self, throttle: int = 0) -> tuple:
        print('###         Login         ###')
        print('Digite "0" (zero) para sair')
        if throttle > 0:
            print('Usuário ou senha incorretos. Tente novamente.')
        login = self._input_str_com_sair('Digite seu e-mail/login: ')
        senha = self._input_str_com_sair('Digite sua senha: ')
        return login, senha, throttle

    def cadastro(self, dados_anteriores={}, erros={}) -> dict:
        print('###         Cadastro         ###')
        print('Digite "0" (zero) para sair')
        if len(dados_anteriores) > 0:
            print('Os seguintes campos estão incorretos:')
        else:
            print('Digite as informações a seguir.')
            print('Campos obrigatórios serão marcados com asterístico (*).')

        campos_errados = [list(erro.keys())[0] for erro in erros]
        mensagens_de_erro = {list(erro.keys())[0]: list(erro.values())[0] for erro in erros}
        dados = copy(dados_anteriores)
        if 'nome' not in dados_anteriores:
            if 'nome' in campos_errados:
                print(mensagens_de_erro['nome'])
            dados['nome'] = self._input_str_com_sair('Nome: * ')
        if 'login' not in dados_anteriores:
            if 'login' in campos_errados:
                print(mensagens_de_erro['login'])
            dados['login'] = self._input_str_com_sair('Login: * ')
        if 'email' not in dados_anteriores:
            if 'email' in campos_errados:
                print(mensagens_de_erro['email'])
            dados['email'] = self._input_str_com_sair('E-mail: * ')
        if 'senha' not in dados_anteriores:
            if 'senha' in campos_errados:
                print(mensagens_de_erro['senha'])
            dados['senha'] = self._input_str_com_sair('Senha: * ')
            dados['confirmacao_senha'] = self._input_str_com_sair('Confirmação de senha: * ')
        if 'cpf' not in dados_anteriores:
            if 'cpf' in campos_errados:
                print(mensagens_de_erro['cpf'])
            dados['cpf'] = self._input_str_com_sair('CPF: * ')
        if 'data_de_nascimento' not in dados_anteriores:
            if 'data_de_nascimento' in campos_errados:
                print(mensagens_de_erro['data_de_nascimento'])
            dados['data_de_nascimento'] = self._input_str_com_sair('Data de nascimento: * ')
        if 'telefone' not in dados_anteriores:
            if 'telefone' in campos_errados:
                print(mensagens_de_erro['telefone'])
            dados['telefone'] = self._input_str_com_sair('Telefone: * ')
        return dados

    @staticmethod
    def sucesso_ao_cadastrar(cliente: dict):
        print(f'Cliente #{cliente["id"]} cadastrado com sucesso!')

    @staticmethod
    def quantidade_de_tentativas_excedidas():
        print('Quantidade de tentativas excedidas!')
