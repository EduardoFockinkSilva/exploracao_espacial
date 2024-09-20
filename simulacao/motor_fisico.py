# motor_fisico.py

from typing import List
from corpo_celeste import CorpoCeleste
import numpy as np


class MotorFisico:
    """
    Classe responsável pela simulação física do sistema.
    """

    def __init__(self, G: float = 6.67430e-20):
        """
        Inicializa o MotorFisico com a constante gravitacional.

        :param G: Constante gravitacional (em km^3 kg^-1 s^-2).
        """
        self.G = G

    def atualizar(self, corpos: List[CorpoCeleste], dt: float) -> None:
        """
        Atualiza as forças gravitacionais e as posições dos corpos celestes.

        :param corpos: Lista de corpos celestes a serem atualizados.
        :param dt: Intervalo de tempo desde a última atualização (em segundos).
        """
        # Aplicar gravidade entre todos os pares de corpos
        for i, corpo_a in enumerate(corpos):
            for j, corpo_b in enumerate(corpos):
                if i != j:
                    corpo_a.aplicar_gravidade(corpo_b, self.G, dt)

        # Atualizar posições e rotações
        for corpo in corpos:
            corpo.atualizar_posicao(dt)
            corpo.atualizar_rotacao(dt)
