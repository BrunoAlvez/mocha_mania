from datetime import datetime

from app.models.cliente import Cliente
from app.models.model_base import ModelBase
from database.seeders.seeder import Seeder


class ClienteSeeder(Seeder):
    @staticmethod
    def run() -> [ModelBase]:
        return [
            Cliente(
                'Cliente',
                'cliente',
                'cliente@email.com',
                '123456789',
                '161.128.410-45',
                datetime.strptime('01/01/2000', '%d/%m/%Y'),
                '(47) 99999-9999',
            )
        ]
