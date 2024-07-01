import PySimpleGUI as sg

from app.views.screens.screen import Screen


class MenuFuncionario(Screen):
    def _layout(self) -> list:
        return [
            [sg.Button('Pedidos', size=(16, 0), key='-PEDIDOS-BUTTON-')],
            [sg.Button('Estoque', size=(16, 0), key='-ESTOQUE-BUTTON-')],
            [sg.Button('Sair', size=(16, 0), key='-SAIR-BUTTON-')],
        ]
