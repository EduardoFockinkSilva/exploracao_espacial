import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from typing import List
from simulacao.objetos.foguete import Foguete
from simulacao.objetos.corpo_celeste import CorpoCeleste
from simulacao.grafico.iluminacao import configurar_luz, aplicar_material, definir_posicao_luz

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
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.largura / self.altura), 1e9, 1e13)
        glMatrixMode(GL_MODELVIEW)

        # Chama a configuração de luz inicial
        configurar_luz()

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

    def desenhar_corpos(self, corpos: list[CorpoCeleste]) -> None:
        """
        Renderiza todos os corpos celestes na tela e define a posição da luz com base no Sol.
        """
        for corpo in corpos:
            if corpo.nome.lower() == "sol":
                # Define a posição da luz como a posição do Sol
                luz_posicao = [corpo.posicao[0], corpo.posicao[1], corpo.posicao[2], 1.0]  # Fonte de luz pontual
                glLightfv(GL_LIGHT0, GL_POSITION, luz_posicao)

                # Configura o Sol para emitir luz (material emissivo)
                emissao_sol = [1.0, 1.0, 0.5, 1.0]  # Cor amarelada
                glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, emissao_sol)
            else:
                # Para os demais corpos, o material emissivo é zero
                emissao_zero = [0.0, 0.0, 0.0, 1.0]
                glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, emissao_zero)

            # Desenhar o corpo celeste ou foguete
            self.desenhar_corpo(corpo)
            self.desenhar_rastro(corpo)

    def desenhar_corpo(self, corpo: CorpoCeleste) -> None:
        """
        Desenha um corpo celeste ou foguete.
        """
        glPushMatrix()

        # Aplica a posição do corpo
        glTranslatef(*corpo.posicao)

       # Define os materiais baseados na cor do corpo
        cor_difusa = [corpo.cor[0] / 255.0, corpo.cor[1] / 255.0, corpo.cor[2] / 255.0, 1.0]
        cor_especular = [1.0, 1.0, 1.0, 1.0]  # Brilho especular branco
        brilho = 50.0  # Brilho especular

        # Aplica o material difuso e especular para que o corpo reaja à luz ambiente e ao Sol
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, cor_difusa)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, cor_especular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, brilho)

        # Verifica se é um foguete para aplicar a orientação e desenhar como pirâmide
        if isinstance(corpo, Foguete):
            # Calcula o ângulo e o eixo de rotação a partir da orientação
            glRotatef(corpo.orientacao[2], 0.0, 0.0, 1.0)  # Rotação em torno do eixo Z (roll)
            glRotatef(corpo.orientacao[1], 0.0, 1.0, 0.0)  # Rotação em torno do eixo Y (yaw)
            glRotatef(corpo.orientacao[0], 1.0, 0.0, 0.0)  # Rotação em torno do eixo X (pitch)

            # Desenha uma pirâmide representando o foguete
            self.desenhar_piramide(corpo.raio * corpo.fator_escala)
        else:
            # Desenha a esfera representando o corpo celeste
            self.desenhar_esfera(corpo.raio * corpo.fator_escala)

        glPopMatrix()

    def desenhar_piramide(self, tamanho: float) -> None:
        """
        Desenha uma pirâmide com o topo apontando para a orientação do foguete, 
        com uma pirâmide menor no topo e uma face colorida para melhor orientação.

        :param tamanho: Escala do tamanho da pirâmide.
        """
        # Vértices da pirâmide principal (parte inferior)
        vertices_principal = [
            (0.0, tamanho, 0.0),  # Topo
            (-tamanho, -tamanho, tamanho),  # Base frontal esquerda
            (tamanho, -tamanho, tamanho),   # Base frontal direita
            (tamanho, -tamanho, -tamanho),  # Base traseira direita
            (-tamanho, -tamanho, -tamanho)  # Base traseira esquerda
        ]

        # Normais das faces principais
        normais_principal = [
            (0.0, 0.4472, tamanho / np.sqrt(2) * 0.4472),  # Frente
            (tamanho / np.sqrt(3), 0.4472, 0.0),  # Direita
            (0.0, 0.4472, -tamanho / np.sqrt(2) * 0.4472),  # Traseira
            (-tamanho / np.sqrt(3), 0.4472, 0.0)  # Esquerda
        ]

        # Desenhar as faces da pirâmide principal
        glBegin(GL_TRIANGLES)
        
        # Frente
        glNormal3fv(normais_principal[0])
        glVertex3fv(vertices_principal[0])
        glVertex3fv(vertices_principal[1])
        glVertex3fv(vertices_principal[2])

        # Direita
        glNormal3fv(normais_principal[1])
        glVertex3fv(vertices_principal[0])
        glVertex3fv(vertices_principal[2])
        glVertex3fv(vertices_principal[3])

        # Traseira
        glNormal3fv(normais_principal[2])
        glVertex3fv(vertices_principal[0])
        glVertex3fv(vertices_principal[3])
        glVertex3fv(vertices_principal[4])

        # Esquerda
        glNormal3fv(normais_principal[3])
        glVertex3fv(vertices_principal[0])
        glVertex3fv(vertices_principal[4])
        glVertex3fv(vertices_principal[1])
        
        glEnd()

        # Desenhar a base da pirâmide principal (quadrado)
        glBegin(GL_QUADS)
        glNormal3f(0.0, -1.0, 0.0)  # Normal para baixo
        glVertex3fv(vertices_principal[1])
        glVertex3fv(vertices_principal[2])
        glVertex3fv(vertices_principal[3])
        glVertex3fv(vertices_principal[4])
        glEnd()

        # Agora desenhar a pirâmide menor no topo da pirâmide principal
        tamanho_menor = tamanho * 0.5  # Tamanho menor da segunda pirâmide no topo

        vertices_menor = [
            (0.0, tamanho * 1.5, 0.0),  # Topo da pirâmide menor
            (-tamanho_menor, tamanho, tamanho_menor),  # Base frontal esquerda
            (tamanho_menor, tamanho, tamanho_menor),   # Base frontal direita
            (tamanho_menor, tamanho, -tamanho_menor),  # Base traseira direita
            (-tamanho_menor, tamanho, -tamanho_menor)  # Base traseira esquerda
        ]

        # Desenhar as faces da pirâmide menor, com a face frontal de outra cor
        glBegin(GL_TRIANGLES)
        
        # Frente (face colorida diferente para ajudar na orientação)
        glColor3f(1.0, 0.0, 0.0)  # Cor vermelha para a face frontal
        glVertex3fv(vertices_menor[0])
        glVertex3fv(vertices_menor[1])
        glVertex3fv(vertices_menor[2])

        # Direita
        glColor3f(1.0, 1.0, 1.0)  # Branco para as outras faces
        glVertex3fv(vertices_menor[0])
        glVertex3fv(vertices_menor[2])
        glVertex3fv(vertices_menor[3])

        # Traseira
        glVertex3fv(vertices_menor[0])
        glVertex3fv(vertices_menor[3])
        glVertex3fv(vertices_menor[4])

        # Esquerda
        glVertex3fv(vertices_menor[0])
        glVertex3fv(vertices_menor[4])
        glVertex3fv(vertices_menor[1])

        glEnd()

        # Desenhar a base da pirâmide menor (quadrado)
        glBegin(GL_QUADS)
        glNormal3f(0.0, -1.0, 0.0)  # Normal para baixo
        glVertex3fv(vertices_menor[1])
        glVertex3fv(vertices_menor[2])
        glVertex3fv(vertices_menor[3])
        glVertex3fv(vertices_menor[4])
        glEnd()

        # Resetar a cor para o padrão após desenhar
        glColor3f(1.0, 1.0, 1.0)


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

                # Normais
                glNormal3f(x, y, np.sin(lat0))
                glVertex3f(x * zr0, y * zr0, z0)
                glNormal3f(x, y, np.sin(lat1))
                glVertex3f(x * zr1, y * zr1, z1)
            glEnd()

    def desenhar_rastro(self, corpo: CorpoCeleste) -> None:
        """
        Desenha o rastro do corpo celeste.
        """
        # Desativar iluminação para o rastro
        glDisable(GL_LIGHTING)
        
        glBegin(GL_LINE_STRIP)
        glColor3ub(*corpo.cor)  # Usa a cor do corpo para o rastro
        for posicao in corpo.rastro:
            glVertex3f(*posicao)
        glEnd()
        
        # Reativar iluminação após desenhar o rastro
        glEnable(GL_LIGHTING)