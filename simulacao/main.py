import pygame
import numpy as np
from simulacao.objetos.corpo_celeste import CorpoCeleste
from simulacao.objetos.foguete import Foguete
from simulacao.grafico.motor_grafico import MotorGrafico
from simulacao.grafico.camera import Camera
from simulacao.motor_fisico import MotorFisico
from simulacao.manipulador_entrada import ManipuladorEntrada
from simulacao.util.gerenciador_dados import carregar_dados_json, criar_corpos_celestes, criar_foguete

posicao_camera = np.array([6e11, 0, 5e10])  # Posição da câmera em um ângulo freten/traz, ,cima/baixo
alvo_camera = np.array([0.0, 0.0, 0.0])
rotacao_camera = np.array([0.0, 0.0, -90.0])  # Rotação em graus

def main():
    pygame.init()

    # Instancia o motor gráfico e o motor físico com tamanho de janela ajustado
    motor_grafico = MotorGrafico(largura=1200, altura=920)
    camera = Camera(posicao=posicao_camera, alvo=alvo_camera, rotacao=rotacao_camera)
    motor_fisico = MotorFisico()
    manipulador_entrada = ManipuladorEntrada()
    #simulacao = Simulacao

    # Carrega os dados dos corpos celestes e foguete a partir do JSON
    dados = carregar_dados_json("simulacao/cenas/solar.json")

    # Cria os corpos celestes
    corpos = criar_corpos_celestes(dados["corpos"])

    # Cria o foguete
    terra = next(corpo for corpo in corpos if corpo.nome == "Terra")
    foguete = criar_foguete(dados["foguete"], terra)

    # Adiciona o foguete à lista de corpos
    corpos.append(foguete)

    # Loop principal
    executando = True
    while executando:
        # Processa eventos usando o ManipuladorEntrada
        executando = manipulador_entrada.processar_eventos(foguete, camera)

        # Verifica se a simulação está pausada
        simulacao_pausada = manipulador_entrada.esta_pausado()
        
        # Atualiza a física somente se a simulação não estiver pausada
        if not simulacao_pausada:
            delta_t = 60 * 60 # Intervalo de tempo em segundos
            motor_fisico.atualizar_corpos(corpos, delta_t)
        else:
            delta_t = 0  # Não avança o tempo quando pausado
        
        # Limpa a tela
        motor_grafico.limpar_tela()
        
        # Atualiza a posição e a rotação da câmera com base nos inputs
        movimento_camera = manipulador_entrada.obter_movimento_camera()
        camera.mover_camera_relativo(movimento_camera)

        # Atualiza a rotação da câmera
        delta_rotacao = manipulador_entrada.obter_rotacao_camera()
        camera.rotacao += delta_rotacao

        # Aplica a nova posição e rotação à matriz de visualização
        camera.ajustar_camera()

        # Desenha os corpos celestes
        motor_grafico.desenhar_corpos(corpos)
        
        # Atualiza a tela
        motor_grafico.atualizar_tela()

    pygame.quit()

if __name__ == "__main__":

    main()
