from __future__ import annotations
from typing import Deque, Tuple, Optional
from collections import deque
import numpy as np

class CorpoCeleste:
    """
    Classe que representa um corpo celeste na simulação.
    """

    def __init__(
        self,
        nome: str,
        massa: float,
        raio: float,
        cor: Tuple[int, int, int],
        fator_escala: float = 1.0,
        a: Optional[float] = None,
        e: Optional[float] = None,
        i_deg: Optional[float] = None,
        massa_central: Optional[float] = None,
        posicao: Optional[np.ndarray] = None,
        velocidade: Optional[np.ndarray] = None,
        max_rastro: int = 1000,
    ):
        """
        Inicializa um novo corpo celeste.

        :param nome: Nome do corpo celeste.
        :param massa: Massa em quilogramas.
        :param raio: Raio em metros.
        :param cor: Cor RGB para representação gráfica.
        :param fator_escala: Fator de escala para visualização.
        :param a: Semi-eixo maior (m). Opcional.
        :param e: Excentricidade. Opcional.
        :param i_deg: Inclinação orbital em graus. Opcional.
        :param massa_central: Massa do corpo central em kg. Necessário se parâmetros orbitais forem fornecidos.
        :param posicao: Vetor posição inicial (np.ndarray). Opcional.
        :param velocidade: Vetor velocidade inicial (np.ndarray). Opcional.
        :param max_rastro: Número máximo de pontos no rastro.
        """
        self.nome: str = nome
        self.massa: float = massa
        self.raio: float = raio
        self.cor: Tuple[int, int, int] = cor
        self.fator_escala: float = fator_escala
        self.rastro: Deque[np.ndarray] = deque(maxlen=max_rastro)

        if a is not None and e is not None and i_deg is not None:
            if massa_central is None:
                raise ValueError("massa_central deve ser fornecida quando parâmetros orbitais são utilizados.")
            # Calcular posição e velocidade a partir dos parâmetros orbitais
            self.posicao, self.velocidade = self.calcular_posicao_velocidade(a, e, i_deg, massa_central)
        elif posicao is not None and velocidade is not None:
            self.posicao = posicao.astype(float)
            self.velocidade = velocidade.astype(float)
        else:
            raise ValueError("Deve fornecer parâmetros orbitais (a, e, i_deg, massa_central) ou posição e velocidade iniciais.")

    def atualizar_posicao(self, delta_t: float) -> None:
        """
        Atualiza a posição do corpo celeste com base em sua velocidade atual.

        :param delta_t: Intervalo de tempo em segundos.
        """
        # Atualiza a posição com base na velocidade atual
        self.posicao += self.velocidade * delta_t
        # Adiciona a nova posição ao rastro
        self.adicionar_ponto_rastro(self.posicao.copy())

    def calcular_forca_gravitacional(self, outro_corpo: CorpoCeleste) -> np.ndarray:
        """
        Calcula a força gravitacional exercida por outro corpo celeste.

        :param outro_corpo: Outro objeto da classe CorpoCeleste.
        :return: Vetor de força gravitacional (np.ndarray).
        """
        G = 6.67430e-11  # Constante gravitacional universal (m^3 kg^-1 s^-2)
        direcao = outro_corpo.posicao - self.posicao
        distancia = np.linalg.norm(direcao)
        if distancia == 0:
            return np.zeros(3)
        forca_magnitude = G * self.massa * outro_corpo.massa / distancia**2
        forca_vetor = (forca_magnitude / distancia) * direcao
        return forca_vetor

    def adicionar_ponto_rastro(self, posicao: np.ndarray) -> None:
        """
        Adiciona um ponto ao rastro do corpo celeste.

        :param posicao: Posição a ser adicionada ao rastro.
        """
        self.rastro.append(posicao)

    @staticmethod
    def calcular_posicao_velocidade(
        a: float, e: float, i_deg: float, massa_central: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula a posição e velocidade inicial de um planeta em órbita.

        :param a: Semi-eixo maior (m).
        :param e: Excentricidade.
        :param i_deg: Inclinação orbital em graus.
        :param massa_central: Massa do corpo central em kg.
        :return: Tupla com posição e velocidade (np.ndarray, np.ndarray).
        """
        G = 6.67430e-11  # Constante gravitacional universal (m^3 kg^-1 s^-2)

        # Converter inclinação para radianos
        i = np.radians(i_deg)

        # Posição inicial no periélio (quando a anomalia verdadeira é zero)
        r = a * (1 - e)
        posicao_orbital = np.array([r, 0, 0])  # Posição no plano orbital

        # Velocidade orbital no periélio
        v = np.sqrt(G * massa_central * (1 + e) / (a * (1 - e)))
        velocidade_orbital = np.array([0, v, 0])  # Velocidade no plano orbital

        # Matriz de rotação para inclinação (rotação em torno do eixo X)
        cos_i = np.cos(i)
        sin_i = np.sin(i)
        matriz_rot = np.array([
            [1, 0,      0     ],
            [0, cos_i, -sin_i],
            [0, sin_i,  cos_i]
        ])

        # Rotacionar posição e velocidade
        posicao = matriz_rot @ posicao_orbital
        velocidade = matriz_rot @ velocidade_orbital

        return posicao, velocidade

    def __repr__(self) -> str:
        return f"CorpoCeleste(nome='{self.nome}', massa={self.massa}, posicao={self.posicao})"
