# foguete.py

from typing import Tuple
from corpo_celeste import CorpoCeleste


class Foguete(CorpoCeleste):
    """
    Classe que representa um foguete, herdando de CorpoCeleste.
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
        Inicializa uma instância de Foguete.

        :param nome: Nome do foguete.
        :param massa: Massa do foguete (em kg).
        :param posicao: Posição no espaço 3D como uma lista [x, y, z] (em km).
        :param velocidade: Velocidade no espaço 3D como uma lista [vx, vy, vz] (em km/s).
        :param raio: Raio do foguete para renderização (em km).
        :param cor: Cor do foguete como tupla (R, G, B) com valores entre 0.0 e 1.0.
        :param inclinacao: Inclinação da órbita em graus.
        :param rotacao_velocidade: Velocidade de rotação em graus por segundo.
        """
        super().__init__(nome, massa, posicao, velocidade, raio, cor, inclinacao, rotacao_velocidade)
        # Propriedades específicas do foguete podem ser adicionadas aqui
        # Por exemplo, combustível, motor, etc.

    # Métodos específicos do foguete podem ser adicionados aqui
    # Por exemplo, método para acionar o motor e alterar a velocidade
