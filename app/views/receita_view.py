from copy import copy

from app.enums.unidade_tempo_enum import UnidadeTempoEnum
from app.helpers.input import input_int
from app.views.view_base import ViewBase


class ReceitaView(ViewBase):
    @staticmethod
    def menu() -> int:
        print('###         Receitas         ###')
        print('Escolha uma opção:')
        return input_int(
            '[1] Listar - [2] Cadastrar - [0] Voltar\n'
        )

    @staticmethod
    def listar(produtos: list):
        if len(produtos) == 0:
            print('Digite "0" (zero) para sair')
            print('Nenhuma receita cadastrada\n')
        else:
            print(' | '.join(['      ID      ', '     Nome     ']))
            for produto in produtos:
                print(' | '.join([str(produto['id']), produto['nome']]))
            print('Digite "0" (zero) para sair')
            print('Digite o ID do produto para mais opções\n')
        return input_int()

    def cadastro(self, ingredientes: list, dados_anteriores={}, erros={}) -> dict:
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
        if 'descricao' not in dados_anteriores:
            if 'descricao' in campos_errados:
                print(mensagens_de_erro['descricao'])
            dados['descricao'] = self._input_str_com_sair('Descrição: * ')
        if 'preco' not in dados_anteriores:
            if 'preco' in campos_errados:
                print(mensagens_de_erro['preco'])
            dados['preco'] = self._input_str_com_sair('Preço: * ')
        if 'preparos' not in dados_anteriores:
            if 'preparos' in campos_errados:
                print(mensagens_de_erro['preparos'])
            dados['preparos'] = self.__incluir_preparos(ingredientes)
        return dados

    @staticmethod
    def __incluir_preparos(ingredientes: list) -> list:
        print('###         Preparos         ###')
        print('Ingredientes disponíveis:')
        for i, ingrediente in enumerate(ingredientes):
            print(f'{i + 1} - {ingrediente["nome"]}')
        preparos = []
        print('Digite "0" (zero) quando terminar de adicionar os preparos.')
        while True:
            ingrediente = input_int('Digite o número do ingrediente: ', 0, len(ingredientes))
            if ingrediente == 0:
                break
            unidade = ingredientes[ingrediente - 1]['unidade']
            print(f'Unidade: {unidade.descricao()}')
            quantidade = input_int('Digite a quantidade: ', 0)
            if quantidade == 0:
                break
            descricao = input('Digite a descrição: ')
            tempo = input_int('Digite o tempo de preparo: ', 0)
            print('Unidade de tempo:')
            for i, unidade in enumerate(UnidadeTempoEnum):
                print(f'{i + 1} - {unidade.descricao()}')
            unidade_tempo = input_int('Digite a unidade de tempo: ', 1, len(UnidadeTempoEnum))
            preparos.append({
                'ingrediente': ingredientes[ingrediente - 1],
                'quantidade': quantidade,
                'unidade': unidade,
                'descricao': descricao,
                'tempo': tempo,
                'unidade_tempo': unidade_tempo,
            })
        return preparos

    @staticmethod
    def sucesso_ao_cadastrar(item: dict):
        print(f"Produto #{item['id']} cadastrado com sucesso!")

    @staticmethod
    def detalhes(item: dict) -> int:
        print('###         Detalhes         ###')
        print(f'ID: {item["id"]}')
        print(f'Nome: {item["nome"]}')
        print(f'Descrição: {item["descricao"]}')
        print(f'Preço: {item["preco"]}')
        return input_int('[1] Atualizar - [2] Remover - [0] Sair\n', 0, 2)

    def atualizacao(self, tipo: int, dados_anteriores={}, erros={}) -> dict:
        print('###         Atualização         ###')
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
        if 'descricao' not in dados_anteriores:
            if 'descricao' in campos_errados:
                print(mensagens_de_erro['descricao'])
            dados['descricao'] = self._input_str_com_sair('Descrição: * ')
        if 'preco' not in dados_anteriores:
            if 'preco' in campos_errados:
                print(mensagens_de_erro['preco'])
            dados['preco'] = self._input_str_com_sair('Preço: * ')
        return dados

    @staticmethod
    def sucesso_ao_atualizar(funcionario: dict):
        print(f"Produto #{funcionario['id']} atualizado com sucesso!")

    @staticmethod
    def remocao() -> int:
        return input_int('Tem certeza que deseja remover o produto?\n[1] - Sim [2] - Não\n')

    @staticmethod
    def sucesso_ao_remover(funcionario: dict):
        print(f"Produto #{funcionario['id']} removido com sucesso!")
