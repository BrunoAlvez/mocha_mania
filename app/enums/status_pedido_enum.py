from app.enums.enum_base import EnumBase


class StatusPedidoEnum(EnumBase):
    PENDENTE = 'pendente'
    PAGO = 'pago'
    EM_PREPARO = 'em_preparo'
    FINALIZADO = 'finalizado'
    ENTREGUE = 'entregue'

    def descricao(self):
        return {
            'pendente': 'Pendente',
            'pago': 'Pago',
            'em_preparo': 'Em preparo',
            'finalizado': 'Finalizado',
            'entregue': 'Entregue',
        }[self.value]
