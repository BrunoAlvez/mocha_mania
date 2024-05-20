from app.enums.unidade_enum import UnidadeEnum
from app.enums.unidade_tempo_enum import UnidadeTempoEnum
from app.models.ingrediente import Ingrediente
from app.models.model_base import ModelBase
from app.models.preparo import Preparo
from app.models.produto import Produto
from database.seeders.seeder import Seeder


class ItensSeeder(Seeder):
    @staticmethod
    def run() -> [ModelBase]:
        ingredientes = [
            Ingrediente(1, 'Farinha de Trigo', 100, UnidadeEnum.QUILOGRAMA),
            Ingrediente(2, 'Ovo', 30, UnidadeEnum.UNIDADE),
            Ingrediente(3, 'Leite', 10, UnidadeEnum.LITRO),
            Ingrediente(4, 'Açúcar', 5, UnidadeEnum.QUILOGRAMA),
            Ingrediente(5, 'Fermento', 1, UnidadeEnum.GRAMA),
            Ingrediente(6, 'Sal', 1, UnidadeEnum.GRAMA),
            Ingrediente(7, 'Óleo', 1, UnidadeEnum.LITRO),
            Ingrediente(8, 'Manteiga', 1, UnidadeEnum.QUILOGRAMA),
            Ingrediente(9, 'Chocolate', 1, UnidadeEnum.QUILOGRAMA),
            Ingrediente(10, 'Café', 1, UnidadeEnum.QUILOGRAMA),
        ]
        preparos = [
            Preparo(
                1,
                ingredientes[0],
                1,
                ingredientes[0].unidade,
                'Peneirar a farinha de trigo',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                2,
                ingredientes[1],
                2,
                ingredientes[1].unidade,
                'Bater os ovos',
                50,
                UnidadeTempoEnum.SEGUNDO,
            ),
            Preparo(
                3,
                ingredientes[2],
                3,
                ingredientes[2].unidade,
                'Aquecer o leite',
                2,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                4,
                ingredientes[3],
                4,
                ingredientes[3].unidade,
                'Adicionar o açúcar',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                5,
                ingredientes[4],
                5,
                ingredientes[4].unidade,
                'Adicionar o fermento',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                6,
                ingredientes[5],
                6,
                ingredientes[5].unidade,
                'Adicionar o sal',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                7,
                ingredientes[6],
                7,
                ingredientes[6].unidade,
                'Adicionar o óleo',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                8,
                ingredientes[7],
                8,
                ingredientes[7].unidade,
                'Adicionar a manteiga',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                9,
                ingredientes[8],
                9,
                ingredientes[8].unidade,
                'Adicionar o chocolate',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                10,
                ingredientes[9],
                10,
                ingredientes[9].unidade,
                'Adicionar o café',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
        ]
        produtos = [
            Produto(11, 'Bala de Chocolate', 1, 'Bala de chocolate', 10.0),
            Produto(12, 'Bala de Chocolate', 2, 'Bala de chocolate', 20.0),
            Produto(13, 'Bala de Café', 3, 'Bala de café', 15.0),
            Produto(14, 'Pão de Queijo', 4, 'Pão de queijo', 5.0),
            Produto(15, 'Pão de Ló', 5, 'Pão de ló', 10.0),
            Produto(16, 'Pão de Mel', 6, 'Pão de mel', 10.0),
            Produto(17, 'Pão', 7, 'Pão fresco', 10.0, [
                preparos[0],
                preparos[1],
                preparos[2],
                preparos[4],
            ]),
            Produto(18, 'Bolo', 8, 'Bolo de chocolate', 20.0, [
                preparos[0],
                preparos[1],
                preparos[2],
                preparos[3],
                preparos[4],
            ]),
            Produto(19, 'Bolo', 9, 'Bolo de café', 20.0, [
                preparos[0],
                preparos[1],
                preparos[2],
                preparos[3],
                preparos[4],
                preparos[9],
            ]),
            Produto(20, 'Bolo', 10, 'Bolo de laranja', 20.0, [
                preparos[0],
                preparos[1],
                preparos[2],
                preparos[3],
                preparos[4],
            ]),
        ]

        return [
            *ingredientes,
            *produtos,
        ]
