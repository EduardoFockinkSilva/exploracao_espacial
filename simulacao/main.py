import numpy as np
from simulacao.corpo_celeste import CorpoCeleste
from simulacao.grafico.motor_grafico import MotorGrafico
from simulacao.motor_fisico import MotorFisico
from simulacao.foguete import Foguete
from simulacao.manipulador_entrada import ManipuladorEntrada
from simulacao.grafico.camera import Camera
import pygame

# Constantes globais
G = 6.67430e-11  # Constante gravitacional universal (m^3 kg^-1 s^-2)

def main():
    pygame.init()

    # Instancia o motor gráfico e o motor físico com tamanho de janela ajustado
    motor_grafico = MotorGrafico(largura=1200, altura=920)
    camera = Camera()
    motor_fisico = MotorFisico()

    # Cria o Sol (fornecendo posição e velocidade diretamente)
    M_SUN = 1.9885e30  # Massa do Sol em kg
    sol = CorpoCeleste(
        nome="Sol",
        massa=M_SUN,
        raio=6.9634e8,
        cor=(255, 255, 0),
        fator_escala=10,  # Fator de escala para visualização do Sol
        posicao=np.array([0.0, 0.0, 0.0]),
        velocidade=np.array([0.0, 0.0, 0.0]),
    )

    # Cria Mercúrio (fornecendo parâmetros orbitais e massa do corpo central)
    mercurio = CorpoCeleste(
        nome="Mercúrio",
        massa=3.3011e23,
        raio=2.4397e6,
        cor=(169, 169, 169),
        fator_escala=500,  # Fator de escala para Mercúrio
        a=5.791e10,
        e=0.2056,
        i_deg=7.0049,
        massa_central=M_SUN,
    )

    # Cria Vênus
    venus = CorpoCeleste(
        nome="Vênus",
        massa=4.8675e24,
        raio=6.0518e6,
        cor=(255, 165, 0),
        fator_escala=500,
        a=1.0821e11,
        e=0.0067,
        i_deg=3.3947,
        massa_central=M_SUN,
    )

    # Cria a Terra
    terra = CorpoCeleste(
        nome="Terra",
        massa=5.9724e24,
        raio=6.3710e6,
        cor=(0, 0, 255),
        fator_escala=500,
        a=1.4959e11,
        e=0.0167,
        i_deg=0.0000,
        massa_central=M_SUN,
    )

    # Cria Marte
    marte = CorpoCeleste(
        nome="Marte",
        massa=6.4171e23,
        raio=3.3895e6,
        cor=(255, 0, 0),
        fator_escala=500,
        a=2.2794e11,
        e=0.0934,
        i_deg=1.8500,
        massa_central=M_SUN,
    )

    # Exemplo de criação de um satélite orbitando a Terra
    # Massa e raio fictícios para o satélite
    satelite = CorpoCeleste(
        nome="Satélite",
        massa=1000,  # Massa em kg
        raio=10,     # Raio em metros
        cor=(0, 255, 0),
        fator_escala=1000,
        a=terra.raio + 4e5,  # Órbita a 400 km da superfície da Terra
        e=0.0,
        i_deg=51.6,  # Inclinação semelhante à da ISS
        massa_central=terra.massa,  # Orbitando a Terra
    )

    # Parâmetros do foguete
    massa_foguete = 2e6  # Massa inicial em kg (incluindo combustível)
    raio_foguete = 1e3   # Raio para visualização
    empuxo_maximo = 3.5e5  # Empuxo máximo em Newtons
    consumo_combustivel = 0  # Consumo de combustível em kg/s
    combustivel_inicial = 1.5e6  # Combustível inicial em kg

    # Posição inicial do foguete (na superfície da Terra)
    posicao_foguete = terra.posicao + np.array([0.0, terra.raio + 1e3, 0.0])
    velocidade_foguete = terra.velocidade  # Inicialmente com a mesma velocidade orbital da Terra
    orientacao_foguete = np.array([0.0, 1.0, 0.0])  # Apontando para "cima"

    foguete = Foguete(
        nome="Foguete",
        massa=massa_foguete,
        raio=raio_foguete,
        cor=(0, 255, 0),
        fator_escala=1.0e6,
        posicao=posicao_foguete,
        velocidade=velocidade_foguete,
        orientacao=orientacao_foguete,
        empuxo_maximo=empuxo_maximo,
        consumo_combustivel=consumo_combustivel,
        combustivel_inicial=combustivel_inicial,
    )

    manipulador_entrada = ManipuladorEntrada()

    # Lista completa de corpos celestes
    corpos = [sol, mercurio, venus, terra, marte, satelite, foguete]

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
        delta_t = 60 * 60  # Intervalo de tempo em segundos
        motor_fisico.atualizar_corpos(corpos, delta_t)
        
        # Limpa a tela
        motor_grafico.limpar_tela()
        
        # Atualiza a posição da câmera com base nos inputs
        movimento_camera = manipulador_entrada.obter_movimento_camera()
        posicao_camera += movimento_camera * delta_t  # Ajuste delta_t conforme necessário

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
