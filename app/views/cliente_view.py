import PySimpleGUI as sg

from app.views.screens.menu_cliente import MenuCliente
from app.views.screens.menu_pedido_cliente import MenuPedidoCliente
from app.views.screens.perfil import Perfil
from app.views.screens.perfil_formulario_atualizacao import PerfilFormularioAtualizacao
from app.views.view_base import ViewBase


class ClienteView(ViewBase):
    def __init__(self, usuario_logado_id: int):
        super().__init__({
            'MENU': MenuCliente(usuario_logado_id),
            'PEDIDO': MenuPedidoCliente(usuario_logado_id),
            'PERFIL': Perfil(usuario_logado_id),
            'ATUALIZAR-PERFIL': PerfilFormularioAtualizacao(usuario_logado_id),
        })
        self.usuario_logado_id = usuario_logado_id

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        if event == '-SAIR-':
            from app.views.sistema_view import SistemaView
            window.hide()
            SistemaView()
        return super().tratar_eventos(event, values, window)
