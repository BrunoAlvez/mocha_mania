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
            Ingrediente('Farinha de Trigo', 100, UnidadeEnum.QUILOGRAMA),
            Ingrediente('Ovo', 30, UnidadeEnum.UNIDADE),
            Ingrediente('Leite', 10, UnidadeEnum.LITRO),
            Ingrediente('Açúcar', 5, UnidadeEnum.QUILOGRAMA),
            Ingrediente('Fermento', 1, UnidadeEnum.GRAMA),
            Ingrediente('Sal', 1, UnidadeEnum.GRAMA),
            Ingrediente('Óleo', 1, UnidadeEnum.LITRO),
            Ingrediente('Manteiga', 1, UnidadeEnum.QUILOGRAMA),
            Ingrediente('Chocolate', 1, UnidadeEnum.QUILOGRAMA),
            Ingrediente('Café', 1, UnidadeEnum.QUILOGRAMA),
        ]
        preparos = [
            Preparo(
                ingredientes[0],
                1,
                ingredientes[0].unidade,
                'Peneirar a farinha de trigo',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                ingredientes[1],
                2,
                ingredientes[1].unidade,
                'Bater os ovos',
                50,
                UnidadeTempoEnum.SEGUNDO,
            ),
            Preparo(
                ingredientes[2],
                3,
                ingredientes[2].unidade,
                'Aquecer o leite',
                2,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                ingredientes[3],
                4,
                ingredientes[3].unidade,
                'Adicionar o açúcar',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                ingredientes[4],
                5,
                ingredientes[4].unidade,
                'Adicionar o fermento',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                ingredientes[5],
                6,
                ingredientes[5].unidade,
                'Adicionar o sal',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                ingredientes[6],
                7,
                ingredientes[6].unidade,
                'Adicionar o óleo',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                ingredientes[7],
                8,
                ingredientes[7].unidade,
                'Adicionar a manteiga',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                ingredientes[8],
                9,
                ingredientes[8].unidade,
                'Adicionar o chocolate',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
            Preparo(
                ingredientes[9],
                10,
                ingredientes[9].unidade,
                'Adicionar o café',
                1,
                UnidadeTempoEnum.MINUTO,
            ),
        ]
        produtos = [
            Produto('Bala de Chocolate', 1, 'Bala de chocolate', 10.0),
            Produto('Bala de Chocolate', 2, 'Bala de chocolate', 20.0),
            Produto('Bala de Café', 3, 'Bala de café', 15.0),
            Produto('Pão de Queijo', 4, 'Pão de queijo', 5.0),
            Produto('Pão de Ló', 5, 'Pão de ló', 10.0),
            Produto('Pão de Mel', 6, 'Pão de mel', 10.0),
            Produto('Pão', 7, 'Pão fresco', 10.0, [
                preparos[0],
                preparos[1],
                preparos[2],
                preparos[4],
            ]),
            Produto('Bolo', 8, 'Bolo de chocolate', 20.0, [
                preparos[0],
                preparos[1],
                preparos[2],
                preparos[3],
                preparos[4],
            ]),
            Produto('Bolo', 9, 'Bolo de café', 20.0, [
                preparos[0],
                preparos[1],
                preparos[2],
                preparos[3],
                preparos[4],
                preparos[9],
            ]),
            Produto('Bolo', 10, 'Bolo de laranja', 20.0, [
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
