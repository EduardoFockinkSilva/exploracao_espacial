import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self, posicao: np.ndarray = np.array([0.0, 0.0, 0.0]), alvo: np.ndarray = np.array([0.0, 0.0, 0.0]), rotacao: np.ndarray = np.array([0.0, 0.0, 0.0])):
        self.posicao = posicao
        self.alvo = alvo
        self.rotacao = rotacao

    def ajustar_camera(self, posicao: np.ndarray, alvo: np.ndarray, rotacao: np.ndarray) -> None:
        """
        Ajusta a posição e a orientação da câmera na cena.
        
        :param posicao: Posição da câmera (eye).
        :param alvo: Alvo para o qual a câmera está olhando (center).
        :param rotacao: Vetor de rotação da câmera em graus nos eixos X, Y e Z.
        """
        self.posicao = posicao
        self.alvo = alvo
        self.rotacao = rotacao
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
