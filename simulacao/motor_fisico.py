from typing import List
import numpy as np
from simulacao.objetos.corpo_celeste import CorpoCeleste
from simulacao.objetos.foguete import Foguete

class MotorFisico:
    """
    Classe responsável pelos cálculos físicos da simulação.
    """

    def __init__(self):
        """
        Inicializa o motor físico.
        """
        pass  # Pode ser utilizado para inicializar parâmetros futuros

    def atualizar_corpos(self, corpos: List[CorpoCeleste], delta_t: float) -> None:
        """
        Atualiza as posições e velocidades dos corpos celestes.
        """
        # Calcula as forças resultantes em cada corpo
        forcas = self.calcular_forcas_gravitacionais(corpos)

        # Atualiza velocidade e posição de cada corpo
        for idx, (corpo, forca_gravitacional) in enumerate(zip(corpos, forcas)):
            # Inicializa a aceleração total com a aceleração gravitacional
            aceleracao_total = forca_gravitacional / corpo.massa

            # Verifica se o corpo é um Foguete
            if isinstance(corpo, Foguete):
                # Atualiza o estado interno do foguete (combustível, massa, etc.)
                corpo.atualizar_estado(delta_t)
                # Adiciona a aceleração devido à propulsão
                aceleracao_total += corpo.aceleracao_propulsao

            # Atualiza a velocidade do corpo
            corpo.velocidade += aceleracao_total * delta_t

            # Atualiza a posição do corpo
            corpo.atualizar_posicao(delta_t)

    def calcular_forcas_gravitacionais(self, corpos: List[CorpoCeleste]) -> List[np.ndarray]:
        """
        Calcula as forças gravitacionais resultantes em cada corpo.

        :param corpos: Lista de corpos celestes na simulação.
        :return: Lista de vetores de força para cada corpo.
        """
        n = len(corpos)
        forcas = [np.zeros(3) for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                corpo_i = corpos[i]
                corpo_j = corpos[j]

                direcao = corpo_j.posicao - corpo_i.posicao
                distancia = np.linalg.norm(direcao)
                if distancia == 0:
                    continue  # Evita divisão por zero

                direcao_unitaria = direcao / distancia

                # Constante gravitacional universal (m^3 kg^-1 s^-2)
                G = 6.67430e-11
                forca_magnitude = G * corpo_i.massa * corpo_j.massa / distancia**2
                forca_vetor = forca_magnitude * direcao_unitaria

                # Aplica a força nos corpos (ação e reação)
                forcas[i] += forca_vetor
                forcas[j] -= forca_vetor

        return forcas
