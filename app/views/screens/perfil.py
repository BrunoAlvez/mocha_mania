import PySimpleGUI as sg

import app.helpers.string as string_helper
from app.controllers.cliente_controller import ClienteController
from app.views.components.sized_box import SizedBox
from app.views.screens.screen import Screen


class Perfil(Screen):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado_id = usuario_logado_id

    def _layout(self) -> list:
        cliente = ClienteController(self.__usuario_logado_id).perfil()
        return [
            [sg.Text('< Voltar', key='-MENU-BUTTON-', font=('Helvetica', 10), size=(0, 0), enable_events=True,
                     expand_x=True)],
            [sg.Text('Perfil')],
            [
                sg.Text('Nome:', size=(12, 0)),
                sg.Text(cliente['nome'], key='-NOME-', colors='white', size=(16, 0)),
            ],
            [
                sg.Text('E-mail:', size=(12, 0)),
                sg.Text(cliente['email'], key='-EMAIL-', colors='white', size=(16, 0)),
            ],
            [
                sg.Text('CPF:', size=(12, 0)),
                sg.Text(cliente['cpf'], key='-CPF-', colors='white', size=(16, 0)),
            ],
            [
                sg.Text('Telefone:', size=(12, 0)),
                sg.Text(cliente['telefone'], key='-TELEFONE-', colors='white', size=(16, 0)),
            ],
            [
                sg.Text('Data de nascimento:', size=(12, 0)),
                sg.Text(string_helper.formatar_data(cliente['data_de_nascimento']), key='-DATA-DE-NASCIMENTO-',
                        colors='white', size=(16, 0)),
            ],
            [sg.Text('Atualizar dados', key='-ATUALIZAR-PERFIL-BUTTON-', font=('Helvetica', 10), size=(0, 0),
                     enable_events=True)],
            [sg.Text('Remover conta', key='-REMOVER-BUTTON-', font=('Helvetica', 10), size=(0, 0), enable_events=True)],
            *SizedBox(height=4),
        ]

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        if event == '-REMOVER-':
            retorno = sg.popup_ok_cancel('Deseja realmente remover a conta?')
            if retorno == 'OK':
                from app.views.sistema_view import SistemaView
                ClienteController(self.__usuario_logado_id).remover()
                window.hide()
                SistemaView()
