import numpy as np
from simulacao.corpo_celeste import CorpoCeleste
from simulacao.grafico.motor_grafico import MotorGrafico
from simulacao.motor_fisico import MotorFisico
from simulacao.foguete import Foguete
from simulacao.manipulador_entrada import ManipuladorEntrada
from simulacao.grafico.camera import Camera
import pygame
import json

# Função para carregar dados do arquivo JSON
def carregar_dados_json(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        return json.load(arquivo)

# Função para criar os corpos celestes a partir dos dados carregados
def criar_corpos_celestes(dados_corpos):
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

# Função para criar o foguete a partir dos dados carregados
def criar_foguete(dados_foguete, terra):
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

def main():
    pygame.init()

    # Instancia o motor gráfico e o motor físico com tamanho de janela ajustado
    motor_grafico = MotorGrafico(largura=1200, altura=920)
    camera = Camera()
    motor_fisico = MotorFisico()
    manipulador_entrada = ManipuladorEntrada()

    # Carrega os dados dos corpos celestes e foguete a partir do JSON
    dados = carregar_dados_json("simulacao\cenas\completo.json")

    # Cria os corpos celestes
    corpos = criar_corpos_celestes(dados["corpos"])

    # Cria o foguete
    terra = next(corpo for corpo in corpos if corpo.nome == "Terra")
    foguete = criar_foguete(dados["foguete"], terra)

    # Adiciona o foguete à lista de corpos
    corpos.append(foguete)

    # Posição inicial da câmera ajustada para visualizar inclinações e órbitas
    posicao_camera = np.array([6e11, 0, 5e10])  # Posição da câmera em um ângulo freten/traz, ,cima/baixo
    alvo_camera = np.array([0.0, 0.0, 0.0])
    rotacao_camera = np.array([0.0, 0.0, -90.0])  # Rotação em graus

    # Loop principal
    executando = True
    while executando:
        # Processa eventos usando o ManipuladorEntrada
        executando = manipulador_entrada.processar_eventos(foguete)
        
        # Atualiza a física
        delta_t = 600  # Intervalo de tempo em segundos
        motor_fisico.atualizar_corpos(corpos, delta_t)
        
        # Limpa a tela
        motor_grafico.limpar_tela()
        
        # Atualiza a posição da câmera com base nos inputs
        movimento_camera = manipulador_entrada.obter_movimento_camera()
        posicao_camera += movimento_camera * 3600  # Ajuste delta_t conforme necessário

        # Atualiza a rotação da câmera
        delta_rotacao = manipulador_entrada.obter_rotacao_camera()
        rotacao_camera += delta_rotacao

        # Aplica a rotação à matriz de visualização
        camera.ajustar_camera(posicao_camera, alvo_camera, rotacao_camera)
        
        # Desenha os corpos celestes
        motor_grafico.desenhar_corpos(corpos)
        
        # Atualiza a tela
        motor_grafico.atualizar_tela()

    pygame.quit()

if __name__ == "__main__":
    main()
