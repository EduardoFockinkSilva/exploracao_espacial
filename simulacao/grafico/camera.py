import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self, posicao: np.ndarray = np.array([0.0, 0.0, 0.0]), alvo: np.ndarray = np.array([0.0, 0.0, 0.0]), rotacao: np.ndarray = np.array([0.0, 0.0, 0.0])):
        self.posicao = posicao
        self.alvo = alvo
        self.rotacao = rotacao

    def atualizar(self) -> None:
        """
        Aplica a rotação e posição da câmera para a cena.
        """
        glLoadIdentity()

        # Aplica as rotações da câmera
        glRotatef(self.rotacao[0], 1.0, 0.0, 0.0)  # Rotação em torno do eixo X
        glRotatef(self.rotacao[1], 0.0, 1.0, 0.0)  # Rotação em torno do eixo Y
        glRotatef(self.rotacao[2], 0.0, 0.0, 1.0)  # Rotação em torno do eixo Z

        # Define a câmera
        gluLookAt(
            self.posicao[0], self.posicao[1], self.posicao[2],
            self.alvo[0], self.alvo[1], self.alvo[2],
            0.0, 1.0, 0.0  # Vetor "up" fixo
        )

    def mover_camera_relativo(self, movimento: np.ndarray) -> None:
        """
        Move a câmera em relação à sua orientação atual (frente, trás, esquerda, direita).

        :param movimento: O vetor de movimento no espaço local da câmera (x, y, z).
        """
        # Converte os ângulos de rotação da câmera em uma matriz de rotação
        yaw = np.radians(self.rotacao[1])  # Rotação em torno do eixo Y (esquerda/direita)
        pitch = np.radians(self.rotacao[0])  # Rotação em torno do eixo X (para cima/baixo)

        # Vetor "frente" da câmera baseado na rotação
        direcao_frente = np.array([
            np.cos(pitch) * np.sin(yaw),
            np.sin(pitch),
            np.cos(pitch) * np.cos(yaw)
        ])

        # Vetor "direita" da câmera baseado na rotação
        direcao_direita = np.array([
            np.cos(yaw),
            0.0,
            -np.sin(yaw)
        ])

        # Vetor "cima" é o vetor cruzado entre "direita" e "frente"
        direcao_cima = np.cross(direcao_direita, direcao_frente)

        # Aplica o movimento relativo às direções da câmera
        self.posicao += movimento[0] * direcao_direita  # Movimento no eixo X
        self.posicao += movimento[1] * direcao_cima     # Movimento no eixo Y
        self.posicao += movimento[2] * direcao_frente   # Movimento no eixo Z
