from app.controllers.controller_base import ControllerBase
from app.enums.status_pedido_enum import StatusPedidoEnum
from app.models.funcionario import Funcionario
from app.services.funcionario_service import FuncionarioService
from app.services.pedido_service import PedidoService


class PedidoController(ControllerBase):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado = FuncionarioService.encontrar(usuario_logado_id)

    @property
    def usuario_logado(self) -> Funcionario:
        return self.__usuario_logado

    @usuario_logado.setter
    def usuario_logado(self, usuario: Funcionario):
        self.__usuario_logado = usuario

    def listar(self, filtros: dict = None):
        pedidos = []
        if filtros is not None:
            if 'apenas_pendentes' in filtros:
                pedidos_pendentes = PedidoService.listar({'status': StatusPedidoEnum.PENDENTE})
                pedidos_em_preparo = PedidoService.listar({'status': StatusPedidoEnum.EM_PREPARO})
                pedidos = pedidos_pendentes + pedidos_em_preparo
        else:
            pedidos = PedidoService.listar()
        pedidos_repositorio = []
        for pedido in pedidos:
            pedidos_repositorio.append(self._repositorio(pedido))
        return pedidos_repositorio

    def assumir(self, id: int):
        PedidoService().assumir(id, self.__usuario_logado)
        return self._repositorio(PedidoService.encontrar(id))

    def finalizar(self, id: int):
        PedidoService().finalizar(id)
        return self._repositorio(PedidoService.encontrar(id))
