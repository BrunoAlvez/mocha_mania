from app.views.screens.historico import Historico
from app.views.view_base import ViewBase


class HistoricoView(ViewBase):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado_id = usuario_logado_id
        super().__init__({
            'INICIO': Historico(usuario_logado_id),
        })
