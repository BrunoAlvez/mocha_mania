import importlib
from enum import Enum

from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.helpers import brasil
from app.helpers import string as string_helper
from datetime import datetime

__traducoes: dict
__validacoes: dict
__erros: list = []


def validar(valores: dict = None, validacoes: dict = None, traducoes: dict = None):
    global __traducoes, __validacoes, __erros

    if valores is None:
        valores = {}
    if validacoes is None:
        validacoes = {}
    if traducoes is None:
        traducoes = {}

    __traducoes = traducoes
    __validacoes = validacoes
    __erros = []

    for atributo, valor in valores.items():
        __validar_regras(atributo, valor)

    if len(__erros) > 0:
        mensagens = [list(erro.values())[0] for erro in __erros]
        raise RegraDeNegocioException('\n'.join(mensagens), dados_extras={'erros': __erros})


def __validar_regras(atributo, valor):
    regras = __validacoes.get(atributo, [])

    if 'nullable' in regras and valor is None:
        return

    if 'required' in regras:
        required(atributo, valor)
    if 'integer' in regras:
        integer(atributo, valor)
    if 'float' in regras:
        double(atributo, valor)
    if 'numeric' in regras:
        numeric(atributo, valor)
    if 'string' in regras:
        string(atributo, valor)
    if 'list' in regras:
        array(atributo, valor)
    if 'email' in regras:
        email(atributo, valor)
    if 'cpf' in regras:
        cpf(atributo, valor)
    if 'date' in regras:
        data(atributo, valor)
    if 'telefone' in regras:
        telefone(atributo, valor)

    for regra in regras:
        if ':' in regra:
            informacoes = regra.split(':')
            if 'min' == informacoes[0]:
                minimo = informacoes[1]
                minimum(atributo, minimo, valor)
            if 'min_or_equal' == informacoes[0]:
                minimo = informacoes[1]
                minimum(atributo, minimo, valor, True)
            if 'max' == informacoes[0]:
                maximo = informacoes[1]
                maximum(atributo, maximo, valor)
            if 'max_or_equal' == informacoes[0]:
                maximo = informacoes[1]
                maximum(atributo, maximo, valor, True)
            if 'instance' == informacoes[0]:
                classe = informacoes[1]
                instance(atributo, valor, classe)
            if 'enum' == informacoes[0]:
                classe_enum = informacoes[1]
                enum(atributo, valor, classe_enum)


def required(atributo, valor):
    if not valor:
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.capitalize()} é obrigatório.')


def integer(atributo, valor):
    if not isinstance(valor, int):
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.capitalize()} deve ser um número inteiro.')


def double(atributo, valor):
    try:
        valor = float(valor)
        if not isinstance(valor, float):
            raise ValueError
    except ValueError:
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.capitalize()} deve ser um número decimal.')

def numeric(atributo, valor):
    if not isinstance(valor, int) and not isinstance(valor, float):
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.capitalize()} deve ser um número.')


def string(atributo, valor):
    if not isinstance(valor, str) and not isinstance(valor, Enum):
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.capitalize()} deve ser uma string.')


def array(atributo, valor):
    if not isinstance(valor, list):
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.capitalize()} deve ser uma lista.')


def email(atributo, valor):
    if '@' not in valor:
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.capitalize()} deve ser um e-mail válido.')


def minimum(atributo, minimo: int, valor, considera_igual=False):
    forca = False
    traducao: str = __traducoes.get(atributo, atributo)
    if isinstance(valor, int) or isinstance(valor, float):
        mensagem = f'O campo {traducao.capitalize()} deve ser no mínimo {minimo}.'
    elif isinstance(valor, str):
        valor = len(valor)
        mensagem = f'O campo {traducao.capitalize()} deve ter no mínimo {minimo} caracteres.'
    elif isinstance(valor, list):
        valor = len(valor)
        mensagem = f'O campo {traducao.capitalize()} deve ter no mínimo {minimo} itens.'
    elif isinstance(valor, dict):
        valor = len(valor)
        mensagem = f'O campo {traducao.capitalize()} deve ter no mínimo {minimo} chaves.'
    else:
        forca = True
        mensagem = f'O tipo do campo {traducao.capitalize()} não é suportado para a regra de mínimo.'

    if forca or valor < int(minimo) or (not considera_igual and valor == minimo):
        __guarda_erro(atributo, mensagem)


def maximum(atributo, maximo: int, valor, considera_igual=False):
    forca = False
    traducao: str = __traducoes.get(atributo, atributo)
    if isinstance(valor, int) or isinstance(valor, float):
        mensagem = f'O campo {traducao.capitalize()} deve ser no máximo {maximo}.'
    elif isinstance(valor, str):
        valor = len(valor)
        mensagem = f'O campo {traducao.capitalize()} deve ter no máximo {maximo} caracteres.'
    elif isinstance(valor, list):
        valor = len(valor)
        mensagem = f'O campo {traducao.capitalize()} deve ter no máximo {maximo} itens.'
    elif isinstance(valor, dict):
        valor = len(valor)
        mensagem = f'O campo {traducao.capitalize()} deve ter no máximo {maximo} chaves.'
    else:
        forca = True
        mensagem = f'O tipo do campo {traducao.capitalize()} não é suportado para a regra de máximo.'

    if forca or valor > int(maximo) or (not considera_igual and valor == maximo):
        __guarda_erro(atributo, mensagem)


def cpf(atributo, valor):
    if not brasil.validar_cpf(valor):
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.upper()} deve ser um CPF válido.')


def data(atributo, valor):
    if isinstance(valor, datetime):
        return

    try:
        eh_data = datetime.strptime(valor, '%d/%m/%Y')
    except ValueError:
        try:
            eh_data = datetime.strptime(valor, '%Y-%m-%d')
        except ValueError:
            eh_data = False
    if not eh_data:
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.capitalize()} deve ser uma data válida.')


def telefone(atributo, valor):
    if not brasil.validar_telefone(valor):
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.capitalize()} deve ser um telefone válido.')


def instance(atributo, valor, classe: str):
    classes = classe.split(',')
    if len(classes) > 1:
        for classe in classes:
            instance(atributo, valor, classe.strip())

    nome_classe = string_helper.pascal_to_snake(classe)
    modulo = importlib.import_module(f'app.models.{nome_classe}')

    if not hasattr(modulo, classe):
        __guarda_erro(atributo, f'A classe {classe} não foi encontrada.')
        return

    if isinstance(valor, list):
        for item in valor:
            instance(atributo, item, classe)

    if not isinstance(valor, getattr(modulo, classe)):
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(atributo, f'O campo {traducao.capitalize()} deve ser uma instância de {classe}.')


def enum(atributo, valor, classe_enum: str):
    nome_enum = string_helper.pascal_to_snake(classe_enum)
    modulo = importlib.import_module(f'app.enums.{nome_enum}')
    itens = getattr(modulo, classe_enum)
    valores = [item.value for item in itens]

    if valor not in valores and valor not in itens:
        traducao: str = __traducoes.get(atributo, atributo)
        __guarda_erro(
            atributo,
            f'O campo {traducao.capitalize()} deve ser um dos seguintes valores: {", ".join(valores).title()}.',
        )


def __guarda_erro(atributo: str, mensagem: str):
    global __erros
    __erros.append({atributo: mensagem})
