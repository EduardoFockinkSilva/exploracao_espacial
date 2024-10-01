import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from typing import List
from simulacao.foguete import Foguete
from simulacao.corpo_celeste import CorpoCeleste

class MotorGrafico:
    """
    Classe responsável pela renderização gráfica dos corpos celestes.
    """

    def __init__(self, largura: int = 800, altura: int = 600, titulo: str = "Simulação do Sistema Solar"):
        """
        Inicializa o motor gráfico e configura a janela de exibição.
        """
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self._inicializar_janela()
        self._configurar_openGL()
        self.clock = pygame.time.Clock()
        self.fps = 60  # Taxa de quadros por segundo

    def _inicializar_janela(self) -> None:
        """
        Inicializa a janela de exibição usando pygame.
        """
        pygame.display.set_mode((self.largura, self.altura), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(self.titulo)

    def _configurar_openGL(self) -> None:
        """
        Configura os parâmetros iniciais do OpenGL.
        """
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto

        # Configuração de projeção ajustada
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.largura / self.altura), 1e9, 1e13)
        glMatrixMode(GL_MODELVIEW)

    def atualizar_tela(self) -> None:
        """
        Atualiza a tela e controla a taxa de quadros.
        """
        pygame.display.flip()
        self.clock.tick(self.fps)

    def limpar_tela(self) -> None:
        """
        Limpa o buffer de cor e profundidade.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def desenhar_corpos(self, corpos: List[CorpoCeleste]) -> None:
        """
        Renderiza todos os corpos celestes na tela.
        """
        for corpo in corpos:
            self.desenhar_corpo(corpo)
            self.desenhar_rastro(corpo)

    def desenhar_corpo(self, corpo: CorpoCeleste) -> None:
        """
        Desenha um corpo celeste ou foguete.
        """
        glPushMatrix()

        # Aplica a posição do corpo
        glTranslatef(*corpo.posicao)

        # Verifica se é um foguete para aplicar a orientação
        if isinstance(corpo, Foguete):
            # Calcula o ângulo e o eixo de rotação a partir da orientação
            orientacao_padrao = np.array([0.0, 1.0, 0.0])  # Orientação padrão
            eixo_rotacao = np.cross(orientacao_padrao, corpo.orientacao)
            angulo = np.degrees(np.arccos(np.dot(orientacao_padrao, corpo.orientacao)))
            if np.linalg.norm(eixo_rotacao) != 0:
                glRotatef(angulo, *eixo_rotacao)
        # Define a cor do corpo
        glColor3ub(*corpo.cor)

        # Desenha a esfera representando o corpo
        self.desenhar_esfera(corpo.raio * corpo.fator_escala)

        glPopMatrix()

    def desenhar_esfera(self, raio: float, slices: int = 20, stacks: int = 20) -> None:
        """
        Desenha uma esfera sem o uso do GLUT.

        :param raio: Raio da esfera.
        :param slices: Número de subdivisões horizontais.
        :param stacks: Número de subdivisões verticais.
        """
        for i in range(0, stacks):
            lat0 = np.pi * (-0.5 + float(i) / stacks)
            z0 = raio * np.sin(lat0)
            zr0 = raio * np.cos(lat0)

            lat1 = np.pi * (-0.5 + float(i + 1) / stacks)
            z1 = raio * np.sin(lat1)
            zr1 = raio * np.cos(lat1)

            glBegin(GL_QUAD_STRIP)
            for j in range(0, slices + 1):
                lng = 2 * np.pi * float(j) / slices
                x = np.cos(lng)
                y = np.sin(lng)

                glNormal3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr0, y * zr0, z0)
                glNormal3f(x * zr1, y * zr1, z1)
                glVertex3f(x * zr1, y * zr1, z1)
            glEnd()

    def desenhar_rastro(self, corpo: CorpoCeleste) -> None:
        """
        Desenha o rastro do corpo celeste.
        """
        glBegin(GL_LINE_STRIP)
        glColor3ub(*corpo.cor)
        for posicao in corpo.rastro:
            glVertex3f(*posicao)
        glEnd()

    def processar_eventos(self) -> bool:
        """
        Processa eventos do pygame, como saída do programa.
        """
        for evento in pygame.event.get():
            if evento.type == QUIT:
                return False
            elif evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    return False
        return True

    def ajustar_camera(self, posicao: np.ndarray, alvo: np.ndarray, rotacao_camera: np.ndarray) -> None:
        """
        Ajusta a posição e a orientação da câmera na cena.

        :param posicao: Posição da câmera (eye).
        :param alvo: Alvo para o qual a câmera está olhando (center).
        :param rotacao_camera: Vetor de rotação da câmera em graus nos eixos X, Y e Z.
        """
        glLoadIdentity()

        # Aplica as rotações da câmera
        glRotatef(rotacao_camera[0], 1.0, 0.0, 0.0)  # Rotação em torno do eixo X
        glRotatef(rotacao_camera[1], 0.0, 1.0, 0.0)  # Rotação em torno do eixo Y
        glRotatef(rotacao_camera[2], 0.0, 0.0, 1.0)  # Rotação em torno do eixo Z

        # Define a câmera
        gluLookAt(
            posicao[0], posicao[1], posicao[2],
            alvo[0], alvo[1], alvo[2],
            0.0, 1.0, 0.0  # Vetor "up" fixo
        )  
