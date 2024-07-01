import PySimpleGUI as sg

import app.helpers.string as string_helper
from app.controllers.cliente_controller import ClienteController
from app.views.components.input_form import InputForm
from app.views.components.sized_box import SizedBox
from app.views.screens.screen import Screen


class PerfilFormularioAtualizacao(Screen):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado = ClienteController(usuario_logado_id).perfil()
        self.__erros = []

    def _layout(self) -> list:
        return [
            [sg.Column(
                [
                    [
                        sg.Text('< Voltar', key='-MENU-BUTTON-', font=('Helvetica', 10), size=(0, 0),
                                enable_events=True),
                    ],
                    *InputForm('Nome', '-NOME-SUBMIT-', valor_inicial=self.__usuario_logado['nome']),
                    *self.__secao_erro('nome'),
                    *InputForm('Telefone', '-TELEFONE-SUBMIT-', enable_events=True,
                               valor_inicial=self.__usuario_logado['telefone']),
                    *self.__secao_erro('telefone'),
                    *SizedBox(height=2),
                    [sg.Button('Atualizar', key='-ATUALIZAR-CLIENTE-BUTTON-', size=(12, 0))]
                ],
                expand_x=True,
                justification='center',
                element_justification='center',
            )],
        ]

    @staticmethod
    def __secao_erro(nome: str):
        nome_secao = nome.replace('_', '-').upper()
        return [
            [sg.Text(
                '',
                key=f'SECAO-{nome_secao}-ERRO-',
                text_color='red',
                size=(48, 0),
                justification='center',
                visible=False,
            )],
            *SizedBox(key=f'-ESPACO-SECAO-{nome_secao}-ERRO-')
        ]

    def tratar_componentes(self, window: sg.Window, key: str):
        componentes_validados = [
            'nome',
            'telefone',
        ]
        for nome in componentes_validados:
            nome_secao = nome.replace('_', '-').upper()
            tem_erros = True in [nome in erro for erro in self.__erros]

            descricao_erro = [erro[nome] for erro in self.__erros if nome in erro] if tem_erros else ''
            if isinstance(descricao_erro, list):
                descricao_erro = '\n'.join(descricao_erro)
            window[f'SECAO-{nome_secao}-ERRO-'].update(
                descricao_erro,
                visible=tem_erros,
            )
            window[f'-ESPACO-SECAO-{nome_secao}-ERRO-'].update(visible=not tem_erros)

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        if event == '-ATUALIZAR-CLIENTE-':
            dados = {
                'nome': values['-NOME-SUBMIT-'],
                'telefone': values['-TELEFONE-SUBMIT-'],
            }
            dados = ClienteController(self.__usuario_logado['id']).atualizar(dados)
            if 'erros' in dados:
                self.__erros = dados['erros']
            else:
                window['-NOME-'].update(dados['nome'])
                window['-TELEFONE-'].update(dados['telefone'])
                self.__erros = []
                return '-PERFIL-'
        elif event == '-TELEFONE-SUBMIT-':
            window[event].update(string_helper.mascara_telefone(values[event]))
