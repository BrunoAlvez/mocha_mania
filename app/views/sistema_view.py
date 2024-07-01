from app.views.screens.cadastro_cliente import CadastroCliente
from app.views.screens.inicio import Inicio
from app.views.screens.inicio_funcionario import InicioFuncionario
from app.views.view_base import ViewBase


class SistemaView(ViewBase):
    def __init__(self):
        super().__init__({
            'INICIO': Inicio(),
            'INICIO-FUNCIONARIO': InicioFuncionario(),
            'CADASTRO-CLIENTE': CadastroCliente(),
        })
