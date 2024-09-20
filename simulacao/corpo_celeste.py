# corpo_celeste.py

from typing import Tuple, List
import numpy as np


class CorpoCeleste:
    """
    Classe que representa um corpo celeste genérico, como planetas ou estrelas.
    """

    def __init__(
        self,
        nome: str,
        massa: float,
        posicao: list,
        velocidade: list,
        raio: float,
        cor: Tuple[float, float, float],
        inclinacao: float = 0.0,  # Inclinação em graus
        rotacao_velocidade: float = 0.0  # Rotação em graus por segundo
    ):
        """
        Inicializa uma instância de CorpoCeleste.

        :param nome: Nome do corpo celeste.
        :param massa: Massa do corpo celeste (em kg).
        :param posicao: Posição no espaço 3D como uma lista [x, y, z] (em km).
        :param velocidade: Velocidade no espaço 3D como uma lista [vx, vy, vz] (em km/s).
        :param raio: Raio do corpo celeste (em km).
        :param cor: Cor do corpo celeste como tupla (R, G, B) com valores entre 0.0 e 1.0.
        :param inclinacao: Inclinação da órbita em graus.
        :param rotacao_velocidade: Velocidade de rotação em graus por segundo.
        """
        self.nome = nome
        self.massa = massa
        self.raio = raio
        self.cor = cor  # Cor do corpo celeste
        self.rotacao_velocidade = rotacao_velocidade  # Rotação em graus por segundo
        self.rotacao_atual = 0.0  # Ângulo atual de rotação
        self.trail: List[np.ndarray] = []  # Lista para armazenar o rastro da trajetória
        self.max_trail_length = 1000  # Número máximo de pontos no rastro

        # Convert lists to numpy arrays
        posicao = np.array(posicao, dtype=float)
        velocidade = np.array(velocidade, dtype=float)

        # Aplicar inclinação
        if inclinacao != 0.0:
            posicao, velocidade = self.aplicar_inclinacao(posicao, velocidade, inclinacao)

        self.posicao = posicao
        self.velocidade = velocidade

        print(f"CorpoCeleste criado: {self.nome}, posição: {self.posicao}, velocidade: {self.velocidade}, raio: {self.raio}, cor: {self.cor}, inclinação: {inclinacao} graus")

    def aplicar_inclinacao(self, posicao: np.ndarray, velocidade: np.ndarray, inclinacao: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Aplica a inclinação à posição e velocidade do corpo celeste.

        :param posicao: Vetor de posição [x, y, z] em km.
        :param velocidade: Vetor de velocidade [vx, vy, vz] em km/s.
        :param inclinacao: Inclinação em graus.
        :return: Tupla (posicao_inclinada, velocidade_inclinada)
        """
        # Converter inclinação para radianos
        inc_rad = np.radians(inclinacao)

        # Matriz de rotação em torno do eixo Z, ajustada para Y invertido
        rot_matrix = np.array([
            [np.cos(inc_rad),  np.sin(inc_rad), 0],
            [-np.sin(inc_rad), np.cos(inc_rad), 0],
            [0,                  0,               1]
        ])

        # Apply rotation
        posicao_inclinada = rot_matrix @ posicao
        velocidade_inclinada = rot_matrix @ velocidade

        print(f"{self.nome} com inclinação aplicada: {inclinacao} graus")
        print(f"Posição inclinada: {posicao_inclinada}")
        print(f"Velocidade inclinada: {velocidade_inclinada}")

        return posicao_inclinada, velocidade_inclinada

    def atualizar_posicao(self, dt: float) -> None:
        """
        Atualiza a posição do corpo celeste com base em sua velocidade e adiciona ao rastro.

        :param dt: Intervalo de tempo desde a última atualização (em segundos).
        """
        self.posicao += self.velocidade * dt
        self.trail.append(self.posicao.copy())
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        #print(f"{self.nome} atualizada para posição: {self.posicao}")

    def aplicar_forca(self, forca: np.ndarray, dt: float) -> None:
        """
        Aplica uma força ao corpo celeste, alterando sua velocidade.

        :param forca: Vetor de força a ser aplicado (em Newtons).
        :param dt: Intervalo de tempo durante o qual a força é aplicada (em segundos).
        """
        aceleracao = forca / self.massa
        self.velocidade += aceleracao * dt
        #print(f"{self.nome} velocidade atualizada para: {self.velocidade}")

    def aplicar_gravidade(self, outro_corpo: 'CorpoCeleste', G: float, dt: float) -> None:
        """
        Aplica a força gravitacional de outro corpo celeste.

        :param outro_corpo: Outro CorpoCeleste que exerce a força.
        :param G: Constante gravitacional (em km^3 kg^-1 s^-2).
        :param dt: Intervalo de tempo (em segundos).
        """
        r_vector = outro_corpo.posicao - self.posicao
        distance = np.linalg.norm(r_vector)
        if distance == 0:
            return  # Evita divisão por zero
        force_magnitude = G * self.massa * outro_corpo.massa / distance**2
        force_direction = r_vector / distance
        force = force_direction * force_magnitude
        self.aplicar_forca(force, dt)
        #print(f"{self.nome} aplicada força gravitacional de {outro_corpo.nome}: {force}")

    def atualizar_rotacao(self, dt: float) -> None:
        """
        Atualiza o ângulo de rotação do corpo celeste.

        :param dt: Intervalo de tempo desde a última atualização (em segundos).
        """
        self.rotacao_atual += self.rotacao_velocidade * dt
        self.rotacao_atual %= 360  # Mantém o ângulo entre 0 e 360
        #print(f"{self.nome} rotacionada para: {self.rotacao_atual} graus")

    def desenhar_trail(self, motor_grafico) -> None:
        """
        Desenha o rastro da trajetória do corpo celeste.

        :param motor_grafico: Instância do MotorGrafico responsável pela renderização.
        """
        motor_grafico.desenhar_trail(self)

    def desenhar(self, motor_grafico) -> None:
        """
        Desenha o corpo celeste e seu rastro utilizando o motor gráfico fornecido.

        :param motor_grafico: Instância do MotorGrafico responsável pela renderização.
        """
        self.desenhar_trail(motor_grafico)
        motor_grafico.desenhar_corpo(self)
