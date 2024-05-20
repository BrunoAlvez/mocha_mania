class RegraDeNegocioException(Exception):
    def __init__(self, mensagem: str, dados_extras: dict = {}):
        super().__init__(mensagem)
        self.__mensagem = mensagem
        self.__dados_extras = dados_extras

    @property
    def mensagem(self) -> str:
        return self.__mensagem

    @property
    def dados_extras(self) -> dict:
        return self.__dados_extras

