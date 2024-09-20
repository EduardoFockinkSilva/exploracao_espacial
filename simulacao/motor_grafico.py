# motor_grafico.py

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from typing import List
from corpo_celeste import CorpoCeleste
import numpy as np


class MotorGrafico:
    """
    Classe responsável pela renderização gráfica em 3D.
    """

    def __init__(self, largura: int = 1920, altura: int = 1080):
        self.largura = largura
        self.altura = altura
        self.janela = None
        self.camera_posicao = np.array([0.0, 0.0, 200.0], dtype=float)  # Posição inicial da câmera em unidades OpenGL
        self.fator_escala = 1e-7  # Escala para converter km para unidades OpenGL
        self.fator_tamanho = 1e-5  # Escala para converter km para o tamanho visual dos objetos

    def inicializar(self) -> None:
        """
        Inicializa o contexto gráfico e configura o OpenGL.
        """
        pygame.init()
        self.janela = pygame.display.set_mode((self.largura, self.altura), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption('Simulador do Sistema Solar')

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Configura a luz
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))  # Luz posicionada na origem (Sol)
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

        # Configura a projeção
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.largura / self.altura), 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

        # Define a cor de fundo
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto

    def atualizar_camera(self) -> None:
        """
        Atualiza a posição e orientação da câmera.
        """
        glLoadIdentity()
        gluLookAt(
            self.camera_posicao[0], self.camera_posicao[1], self.camera_posicao[2],  # Posição da câmera
            0.0, 0.0, 0.0,   # Ponto para onde a câmera está olhando (origem)
            0.0, 1.0, 0.0    # Vetor "up"
        )

    def desenhar_corpo(self, corpo: CorpoCeleste) -> None:
        """
        Desenha um corpo celeste na cena.

        :param corpo: Instância de CorpoCeleste a ser desenhada.
        """
        glPushMatrix()
        posicao_escalada = corpo.posicao * self.fator_escala
        glTranslatef(*posicao_escalada)

        # Aplica a rotação
        glRotatef(corpo.rotacao_atual, 0, 1, 0)  # Rotaciona em torno do eixo Y

        # Define a cor do corpo
        glColor3f(*corpo.cor)

        # Define o tamanho aparente com tamanho mínimo
        min_display_radius = 0.5  # Unidade mínima para visualização
        display_radius = max(corpo.raio * self.fator_tamanho, min_display_radius)

        # Desenha a esfera
        quadric = gluNewQuadric()
        gluSphere(quadric, display_radius, 32, 32)
        gluDeleteQuadric(quadric)

        glPopMatrix()

    def desenhar_trajetoria(self, corpo: CorpoCeleste) -> None:
        """
        Desenha a trajetória de um corpo celeste.

        :param corpo: Instância de CorpoCeleste cuja trajetória será desenhada.
        """
        if len(corpo.trajetoria) < 2:
            return  # Não há trajetória suficiente para desenhar

        glColor3f(*corpo.cor)  # Usa a mesma cor do corpo para a trajetória
        glBegin(GL_LINE_STRIP)
        for pos in corpo.trajetoria:
            pos_escalada = pos * self.fator_escala
            glVertex3f(*pos_escalada)
        glEnd()

    def renderizar(self, corpos: List[CorpoCeleste]) -> None:
        """
        Renderiza todos os corpos celestes na cena.

        :param corpos: Lista de instâncias de CorpoCeleste a serem renderizadas.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.atualizar_camera()

        # Adiciona rotação global para visualização dinâmica
        glRotatef(pygame.time.get_ticks() / 1000 * 10, 0, 1, 0)  # Rotaciona 10 graus por segundo em torno do eixo Y

        for corpo in corpos:
            corpo.desenhar(self)
            self.desenhar_trajetoria(corpo)

        pygame.display.flip()

    def processar_eventos(self) -> bool:
        """
        Processa eventos do Pygame, como fechamento da janela e controles de câmera.

        :return: False se o usuário solicitar o fechamento da janela, True caso contrário.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                elif evento.key == pygame.K_UP:
                    self.camera_posicao[2] -= 10.0  # Aproxima a câmera
                elif evento.key == pygame.K_DOWN:
                    self.camera_posicao[2] += 10.0  # Afasta a câmera
        return True
