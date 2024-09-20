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
        rotacao_velocidade: float = 0.0,  # Rotação em graus por segundo
        inclinacao: float = 0.0  # Inclinação orbital em graus
    ):
        """
        Inicializa uma instância de CorpoCeleste.

        :param nome: Nome do corpo celeste.
        :param massa: Massa do corpo celeste (em kg).
        :param posicao: Posição no espaço 3D como uma lista [x, y, z] (em km).
        :param velocidade: Velocidade no espaço 3D como uma lista [vx, vy, vz] (em km/s).
        :param raio: Raio do corpo celeste (em km).
        :param cor: Cor do corpo celeste como tupla (R, G, B) com valores entre 0.0 e 1.0.
        :param rotacao_velocidade: Velocidade de rotação em graus por segundo.
        :param inclinacao: Inclinação orbital em graus.
        """
        self.nome = nome
        self.massa = massa
        self.posicao = np.array(posicao, dtype=float)
        self.velocidade = np.array(velocidade, dtype=float)
        self.raio = raio
        self.cor = cor  # Cor do corpo celeste
        self.rotacao_velocidade = rotacao_velocidade  # Rotação em graus por segundo
        self.rotacao_atual = 0.0  # Ângulo atual de rotação
        self.inclinacao = inclinacao  # Inclinação orbital em graus
        self.trajetoria: List[np.ndarray] = []  # Lista para armazenar posições anteriores

        # Aplica a inclinação à posição e velocidade
        self.inicializar_inclinacao()

        print(f"CorpoCeleste criado: {self.nome}, posição: {self.posicao}, "
              f"raio: {self.raio}, cor: {self.cor}, inclinação: {self.inclinacao} graus")

    def inicializar_inclinacao(self) -> None:
        """
        Aplica a inclinação orbital à posição e velocidade iniciais.
        """
        if self.inclinacao != 0.0:
            # Converter a inclinação para radianos
            inclinacao_rad = np.radians(self.inclinacao)

            # Matriz de rotação para inclinação em torno do eixo X
            rot_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(inclinacao_rad), -np.sin(inclinacao_rad)],
                [0, np.sin(inclinacao_rad), np.cos(inclinacao_rad)]
            ])

            # Aplicar rotação à posição e velocidade
            self.posicao = rot_matrix @ self.posicao
            self.velocidade = rot_matrix @ self.velocidade
            print(f"{self.nome} inclinada pela matriz de rotação:\n{rot_matrix}")

    def atualizar_posicao(self, dt: float) -> None:
        """
        Atualiza a posição do corpo celeste com base em sua velocidade.

        :param dt: Intervalo de tempo desde a última atualização (em segundos).
        """
        self.posicao += self.velocidade * dt
        self.trajetoria.append(self.posicao.copy())

        # Limita o tamanho da trajetória para evitar consumo excessivo de memória
        if len(self.trajetoria) > 1000:
            self.trajetoria.pop(0)

        print(f"{self.nome} atualizada para posição: {self.posicao}")

    def aplicar_forca(self, forca: np.ndarray, dt: float) -> None:
        """
        Aplica uma força ao corpo celeste, alterando sua velocidade.

        :param forca: Vetor de força a ser aplicado (em Newtons).
        :param dt: Intervalo de tempo durante o qual a força é aplicada (em segundos).
        """
        aceleracao = forca / self.massa
        self.velocidade += aceleracao * dt
        print(f"{self.nome} velocidade atualizada para: {self.velocidade}")

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
        print(f"{self.nome} aplicada força gravitacional de {outro_corpo.nome}: {force}")

    def atualizar_rotacao(self, dt: float) -> None:
        """
        Atualiza o ângulo de rotação do corpo celeste.

        :param dt: Intervalo de tempo desde a última atualização (em segundos).
        """
        self.rotacao_atual += self.rotacao_velocidade * dt
        self.rotacao_atual %= 360  # Mantém o ângulo entre 0 e 360
        print(f"{self.nome} rotacionada para: {self.rotacao_atual} graus")

    def desenhar(self, motor_grafico) -> None:
        """
        Desenha o corpo celeste utilizando o motor gráfico fornecido.

        :param motor_grafico: Instância do MotorGrafico responsável pela renderização.
        """
        motor_grafico.desenhar_corpo(self)
