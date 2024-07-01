import PySimpleGUI as sg

from app.views.cliente_view import ClienteView
from app.views.components.input_form import InputForm
from app.views.components.sized_box import SizedBox
from app.views.screens.screen import Screen


class Inicio(Screen):
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
            *InputForm('Login/E-mail', key='-LOGIN-SUBMIT-'),
            *InputForm('Senha', key='-SENHA-SUBMIT-', password=True),
            [sg.Text(
                'Não conseguimos encontrar um usuário com essas credenciais. Tente novamente.',
                key='-ERRO-LOGIN-',
                text_color='red',
                size=(48, 0),
                justification='center',
            )],
            *SizedBox(key='-ESPACO-SECAO-LOGIN-ERRO-'),
            *SizedBox(height=2),
            [sg.Button('Entrar', key='-ENTRAR-BUTTON-', size=(12, 0))],
            [sg.Text('Quero me cadastrar', key='-CADASTRO-CLIENTE-BUTTON-', justification='center',
                     enable_events=True, relief=sg.RELIEF_FLAT)],
            [sg.Text('Sou funcionário', key='-INICIO-FUNCIONARIO-BUTTON-', justification='center',
                     enable_events=True, relief=sg.RELIEF_FLAT)],
        ]

    def tratar_componentes(self, window: sg.Window, key: str):
        window[key].expand(expand_x=True, expand_y=False)
        tem_erros = bool(self.__erros)
        window['-ERRO-LOGIN-'].update(visible=tem_erros)
        window['-ESPACO-SECAO-LOGIN-ERRO-'].update(visible=not tem_erros)

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        from app.controllers.sistema_controller import SistemaController
        if event == '-ENTRAR-':
            dados = {
                'login': values['-LOGIN-SUBMIT-'],
                'senha': values['-SENHA-SUBMIT-'],
            }
            retorno = SistemaController().login_cliente(dados, self.__throttle)
            if 'erros' in retorno:
                self.__erros = retorno['erros']
                self.__throttle = retorno['throttle']
            elif 'usuario.id' in retorno:
                self.__erros = {}
                self.__throttle = 0
                window.hide()
                ClienteView(retorno['usuario.id'])
