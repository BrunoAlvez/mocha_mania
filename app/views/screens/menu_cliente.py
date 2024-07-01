import PySimpleGUI as sg

from app.views.components.sized_box import SizedBox
from app.views.historico_view import HistoricoView
from app.views.screens.screen import Screen


class MenuCliente(Screen):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado_id = usuario_logado_id

    def _layout(self) -> list:
        return [
            *SizedBox(height=4),
            [sg.Button('Pedir', size=(16, 0), key='-PEDIDO-BUTTON-')],
            [sg.Button('Histórico', size=(16, 0), key='-HISTORICO-BUTTON-')],
            [sg.Button('Perfil', size=(16, 0), key='-PERFIL-BUTTON-')],
            [sg.Button('Sair', size=(16, 0), key='-SAIR-BUTTON-')],
        ]

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        if event == '-HISTORICO-':
            window.hide()
            HistoricoView(self.__usuario_logado_id)
