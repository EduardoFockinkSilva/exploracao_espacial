# main.py

import sys
from corpo_celeste import CorpoCeleste
from foguete import Foguete
from motor_fisico import MotorFisico
from motor_grafico import MotorGrafico
import pygame


def main():
    # Inicializa os motores
    motor_grafico = MotorGrafico()
    motor_grafico.inicializar()

    motor_fisico = MotorFisico()

    # Cria instâncias de CorpoCeleste com inclinações diferentes
    sol = CorpoCeleste(
        nome='Sol',
        massa=1.989e30,  # Massa do Sol em kg
        posicao=[0.0, 0.0, 0.0],  # Posição na origem em km
        velocidade=[0.0, 0.0, 0.0],  # Velocidade inicial em km/s
        raio=696340.0,  # Raio do Sol em km
        cor=(1.0, 1.0, 0.0),  # Cor amarela
        rotacao_velocidade=10.0,  # Rotação de 10 graus por segundo
        inclinacao=0.0  # Inclinação orbital do Sol (não se aplica, mas mantido para consistência)
    )

    terra = CorpoCeleste(
        nome='Terra',
        massa=5.972e24,  # Massa da Terra em kg
        posicao=[149600000.0, 0.0, 0.0],  # Distância média do Sol em km
        velocidade=[0.0, 29.78, 0.0],  # Velocidade orbital em km/s
        raio=6371.0,  # Raio da Terra em km
        cor=(0.0, 0.0, 1.0),  # Cor azul
        rotacao_velocidade=30.0,  # Rotação de 30 graus por segundo
        inclinacao=45.0  # Inclinação orbital da Terra em graus
    )

    # Cria instância do Foguete com inclinação
    foguete = Foguete(
        nome='Foguete',
        massa=50000.0,  # Massa do foguete em kg
        posicao=[149600000.0 + 7000.0, 0.0, 0.0],  # Posicionado próximo à Terra (7000 km acima)
        velocidade=[0.0, 29.78 + 7.8, 0.0],  # Velocidade orbital mais 7.8 km/s para órbita baixa
        raio=2.0,  # Raio do foguete em km (ajustado para visibilidade)
        cor=(1.0, 0.0, 0.0),  # Cor vermelha
        rotacao_velocidade=100.0,  # Rotação rápida para efeito visual
        inclinacao=5.0  # Inclinação orbital do foguete em graus
    )

    # Lista de corpos para renderização
    corpos = [sol, terra, foguete]

    # Loop principal
    clock = pygame.time.Clock()
    executando = True
    while executando:
        executando = motor_grafico.processar_eventos()

        # Obtém o intervalo de tempo desde a última atualização
        dt = clock.get_time() / 1000.0  # dt em segundos

        # Atualiza física
        motor_fisico.atualizar(corpos, dt)

        # Renderiza a cena
        motor_grafico.renderizar(corpos)

        # Controla a taxa de quadros (FPS)
        clock.tick(60)  # Limita a 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
