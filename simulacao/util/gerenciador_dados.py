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
        if "velocidade" in corpo:
            corpos.append(CorpoCeleste(
                nome=corpo["nome"],
                massa=corpo["massa"],
                raio=corpo["raio"],
                cor=tuple(corpo["cor"]),
                fator_escala=corpo["fator_escala"],
                posicao=np.array(corpo["posicao"]),
                velocidade=np.array(corpo["velocidade"]),
            ))
        else:
            corpos.append(CorpoCeleste(
                nome=corpo["nome"],
                massa=corpo["massa"],
                raio=corpo["raio"],
                cor=tuple(corpo["cor"]),
                fator_escala=corpo["fator_escala"],
                a=corpo["a"],
                e=corpo["e"],
                i_deg=corpo["i_deg"],
                massa_central=corpo["massa_central"]
            ))
    return corpos

def criar_foguete(dados_foguete, terra):
    """
    Cria um objeto Foguete a partir dos dados carregados.
    """
    posicao_foguete = terra.posicao + np.array(dados_foguete["posicao_inicial"])
    return Foguete(
        nome=dados_foguete["nome"],
        massa=dados_foguete["massa"],
        raio=dados_foguete["raio"],
        cor=tuple(dados_foguete["cor"]),
        fator_escala=dados_foguete["fator_escala"],
        posicao=posicao_foguete,
        velocidade=terra.velocidade,  # Inicialmente com a mesma velocidade orbital da Terra
        orientacao=np.array(dados_foguete["orientacao_inicial"]),
        empuxo_maximo=dados_foguete["empuxo_maximo"],
        consumo_combustivel=dados_foguete["consumo_combustivel"],
        combustivel_inicial=dados_foguete["combustivel_inicial"],
    )
