import PySimpleGUI as sg

from app.views.screens.estoque_atual import EstoqueAtual
from app.views.screens.menu_funcionario import MenuFuncionario
from app.views.screens.pedidos_pendentes import PedidosPendentes
from app.views.view_base import ViewBase


class FuncionarioView(ViewBase):
    def __init__(self, usuario_logado_id: int):
        super().__init__({
            'MENU': MenuFuncionario(),
            'PEDIDOS': PedidosPendentes(usuario_logado_id),
            'ESTOQUE': EstoqueAtual(usuario_logado_id),
        })
        self.__usuario_logado_id = usuario_logado_id

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        if event == '-SAIR-':
            from app.views.sistema_view import SistemaView
            window.hide()
            SistemaView()
        return super().tratar_eventos(event, values, window)
