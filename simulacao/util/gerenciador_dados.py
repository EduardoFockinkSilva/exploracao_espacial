import json
import numpy as np
from simulacao.objetos.corpo_celeste import CorpoCeleste
from simulacao.objetos.foguete import Foguete

def carregar_dados_json(caminho_arquivo):
    """
    Carrega os dados do sistema solar a partir de um arquivo JSON.
    """
    with open(caminho_arquivo, 'r') as arquivo:
        return json.load(arquivo)

def criar_corpos_celestes(dados_corpos):
    """
    Cria os objetos de CorpoCeleste a partir dos dados carregados.
    """
    corpos = []
    for corpo in dados_corpos:
        if "velocidade" in corpo and "posicao" in corpo:
            corpos.append(CorpoCeleste(
                nome=corpo["nome"],
                massa=corpo["massa"],
                raio=corpo["raio"],
                cor=tuple(corpo["cor"]),
                fator_escala=corpo.get("fator_escala", 1.0),
                posicao=np.array(corpo["posicao"]),
                velocidade=np.array(corpo["velocidade"]),
                brilho=corpo.get("brilho", 1.0),
            ))
        else:
            corpos.append(CorpoCeleste(
                nome=corpo["nome"],
                massa=corpo["massa"],
                raio=corpo["raio"],
                cor=tuple(corpo["cor"]),
                fator_escala=corpo.get("fator_escala", 1.0),
                a=corpo.get("a"),
                e=corpo.get("e"),
                i_deg=corpo.get("i_deg"),
                massa_central=corpo.get("massa_central"),
                brilho=corpo.get("brilho", 1.0),
            ))
    return corpos

def criar_foguete(dados_foguete, planeta_origem, destino=None):
    """
    Cria um objeto Foguete a partir dos dados carregados.

    :param dados_foguete: Dicionário com os dados do foguete.
    :param planeta_origem: CorpoCeleste a partir do qual o foguete é lançado.
    :param destino: Posição (np.ndarray) ou CorpoCeleste destino do foguete.
    :return: Instância de Foguete.
    """
    posicao_foguete = planeta_origem.posicao + np.array(dados_foguete["posicao_inicial"])

    # Define a velocidade inicial
    if destino is None or not isinstance(destino, CorpoCeleste):
        velocidade_inicial = planeta_origem.velocidade.copy()
    else:
        velocidade_inicial = destino.velocidade.copy()

    return Foguete(
        nome=dados_foguete["nome"],
        massa=dados_foguete["massa"],
        raio=dados_foguete["raio"],
        cor=tuple(dados_foguete["cor"]),
        fator_escala=dados_foguete.get("fator_escala", 1.0),
        posicao=posicao_foguete,
        velocidade=velocidade_inicial,
        orientacao=np.array(dados_foguete["orientacao_inicial"]),
        empuxo_maximo=dados_foguete["empuxo_maximo"],
        consumo_combustivel=dados_foguete["consumo_combustivel"],
        combustivel_inicial=dados_foguete["combustivel_inicial"],
        destino=destino,
    )
