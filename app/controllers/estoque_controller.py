from app.controllers.controller_base import ControllerBase
from app.enums.cargo_enum import CargoEnum
from app.models.item import Item
from app.models.produto import Produto
from app.services.funcionario_service import FuncionarioService
from app.services.item_service import ItemService


class EstoqueController(ControllerBase):
    def __init__(self, usuario_logado_id: int = None):
        self.__usuario_logado = None
        if usuario_logado_id is not None:
            self.__usuario_logado = FuncionarioService.encontrar(usuario_logado_id)

    def listar(self, filtros: dict = None) -> list[dict]:
        itens = ItemService.listar(filtros if filtros is not None else {})
        itens_repositorio = []
        for item in itens:
            repositorio = self._repositorio(item)
            repositorio['tipo'] = 'Produto' if isinstance(item, Produto) else 'Ingrediente'
            itens_repositorio.append(repositorio)
        return itens_repositorio

    def listar_produtos(self) -> list[dict]:
        return self.listar({'apenas_produtos': True})

    def reabastecer(self, item_id: int, quantidade: float):
        item_atualizado = ItemService().reabastecer(item_id, quantidade)
        return self._repositorio(item_atualizado)

    def verificar_permissao_para_reabastecer(self):
        return self.__usuario_logado.cargo == CargoEnum.GERENTE

    def _repositorio(self, item: Item):
        dados = super()._repositorio(item)
        dados['tipo'] = 'Produto' if isinstance(item, Produto) else 'Ingrediente'
        dados['disponivel'] = ItemService().verificar_disponibilidade(item)
        return dados
