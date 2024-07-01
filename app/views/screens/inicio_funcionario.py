import PySimpleGUI as sg

from app.views.components.input_form import InputForm
from app.views.components.sized_box import SizedBox
from app.views.funcionario_view import FuncionarioView
from app.views.screens.screen import Screen


class InicioFuncionario(Screen):
    def __init__(self):
        self.__erros = {}
        self.__throttle = 0

    def _layout(self) -> list:
        return [
            *SizedBox(height=2),
            [sg.Text('MOCHA MANIA', font=('Helvetica', 16), justification='center', size=(48, 0))],
            [sg.Text('O portal de vendas de café mais completo do Brasil!', font=('Helvetica', 10),
                     justification='center', size=(48, 0))],
            *SizedBox(height=8),
            *InputForm('Login/E-mail', key='-LOGIN-FUNCIONARIO-SUBMIT-'),
            *InputForm('Senha', key='-SENHA-FUNCIONARIO-SUBMIT-', password=True),
            [sg.Text(
                'Não conseguimos encontrar um usuário com essas credenciais. Tente novamente.',
                key='-ERRO-LOGIN-FUNCIONARIO-',
                text_color='red',
                size=(48, 0),
                justification='center',
            )],
            *SizedBox(key='-ESPACO-SECAO-LOGIN-FUNCIONARIO-ERRO-'),
            *SizedBox(height=2),
            [sg.Button('Entrar', key='-ENTRAR-FUNCIONARIO-BUTTON-', size=(12, 0))],
            [sg.Text('< Voltar', key='-INICIO-BUTTON-', justification='center', enable_events=True,
                     relief=sg.RELIEF_FLAT)],
        ]

    def tratar_componentes(self, window: sg.Window, key: str):
        window[key].expand(expand_x=True, expand_y=False)
        tem_erros = bool(self.__erros)
        window['-ERRO-LOGIN-FUNCIONARIO-'].update(visible=tem_erros)
        window['-ESPACO-SECAO-LOGIN-FUNCIONARIO-ERRO-'].update(visible=not tem_erros)

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        from app.controllers.sistema_controller import SistemaController
        if event == '-ENTRAR-FUNCIONARIO-':
            dados = {
                'login': values['-LOGIN-FUNCIONARIO-SUBMIT-'],
                'senha': values['-SENHA-FUNCIONARIO-SUBMIT-'],
            }
            retorno = SistemaController().login_funcionario(dados, self.__throttle)
            if 'erros' in retorno:
                self.__erros = retorno['erros']
                self.__throttle = retorno['throttle']
            elif 'usuario.id' in retorno:
                self.__erros = {}
                self.__throttle = 0
                window.hide()
                FuncionarioView(retorno['usuario.id'])
