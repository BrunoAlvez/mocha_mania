import PySimpleGUI as sg

import app.helpers.string as string_helper
from app.views.components.input_form import InputForm
from app.views.components.sized_box import SizedBox
from app.views.screens.screen import Screen


class CadastroCliente(Screen):
    def __init__(self):
        self.__erros = {}

    @property
    def erros(self):
        return self.__erros

    def _layout(self) -> list:
        return [
            [sg.Column(
                [
                    [sg.Text('< Voltar', key='-INICIO-BUTTON-', font=('Helvetica', 10), size=(0, 0),
                             enable_events=True)],
                    *InputForm('Nome', '-NOME-SUBMIT-'),
                    *self.__secao_erro('nome'),
                    *InputForm('Login', '-LOGIN-CADASTRO-SUBMIT-'),
                    *self.__secao_erro('login'),
                    *InputForm('E-mail', '-EMAIL-SUBMIT-'),
                    *self.__secao_erro('email'),
                    *InputForm('Senha', '-SENHA-CADASTRO-SUBMIT-', password=True),
                    *self.__secao_erro('senha'),
                    *InputForm('Confirmação de senha', '-CONFIRMACAO-SENHA-SUBMIT-', password=True),
                    *self.__secao_erro('confirmacao_senha'),
                    *InputForm('CPF', '-CPF-SUBMIT-', enable_events=True),
                    *self.__secao_erro('cpf'),
                    *InputForm('Data de nascimento', '-DATA-DE-NASCIMENTO-SUBMIT-', enable_events=True),
                    *self.__secao_erro('data_de_nascimento'),
                    *InputForm('Telefone', '-TELEFONE-SUBMIT-', enable_events=True),
                    *self.__secao_erro('telefone'),
                    *SizedBox(height=2),
                    [sg.Button('Cadastrar', key='-CADASTRAR-CLIENTE-BUTTON-', size=(12, 0))]
                ],
                scrollable=True,
                vertical_scroll_only=True,
                expand_y=True,
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
        window[key].expand(expand_x=True, expand_y=True)
        window['-INICIO-BUTTON-'].expand(expand_x=True, expand_y=False)

        componentes_validados = [
            'nome',
            'login',
            'email',
            'senha',
            'confirmacao_senha',
            'cpf',
            'data_de_nascimento',
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
        from app.controllers.sistema_controller import SistemaController
        if event == '-CADASTRAR-CLIENTE-':
            dados = {
                'nome': values['-NOME-SUBMIT-'],
                'login': values['-LOGIN-CADASTRO-SUBMIT-'],
                'email': values['-EMAIL-SUBMIT-'],
                'senha': values['-SENHA-CADASTRO-SUBMIT-'],
                'confirmacao_senha': values['-CONFIRMACAO-SENHA-SUBMIT-'],
                'cpf': values['-CPF-SUBMIT-'],
                'data_de_nascimento': values['-DATA-DE-NASCIMENTO-SUBMIT-'],
                'telefone': values['-TELEFONE-SUBMIT-'],
            }
            dados = SistemaController().cadastrar(dados)
            if 'erros' in dados:
                self.__erros = dados['erros']
        elif event == '-TELEFONE-SUBMIT-':
            window[event].update(string_helper.mascara_telefone(values[event]))
        elif event == '-CPF-SUBMIT-':
            window[event].update(string_helper.mascara_cpf(values[event]))
        elif event == '-DATA-DE-NASCIMENTO-SUBMIT-':
            window[event].update(string_helper.mascara_data(values[event]))
