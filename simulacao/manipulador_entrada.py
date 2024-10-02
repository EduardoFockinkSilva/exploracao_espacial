import pygame
import numpy as np
from simulacao.objetos.foguete import Foguete

class ManipuladorEntrada:
    """
    Classe responsável por gerenciar os inputs do usuário.
    """
    def __init__(self):
        """
        Inicializa o ManipuladorEntrada.
        """
        self.teclas_pressionadas = set()
        self.movimento_camera = np.array([0.0, 0.0, 0.0])
        self.rotacao_camera = np.array([0.0, 0.0, 0.0])  # Rotação em torno dos eixos X, Y, Z
        self.vetor_up = np.array([0.0, 0.0, 0.0])

        # Multiplicador para a velocidade de rotação do foguete
        self.multiplicador_rotacao_foguete = 1.0

    def processar_eventos(self, foguete: Foguete) -> bool:
        """
        Processa eventos do pygame, como saída do programa e controles do foguete e da câmera.

        :param foguete: Instância do foguete a ser controlado.
        :return: False se o usuário solicitar sair, True caso contrário.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                self.teclas_pressionadas.add(evento.key)
                # Seção dos controles gerais (ESC, menus)
                if evento.key == pygame.K_ESCAPE:
                    return False
                # Seção dos controles do foguete
                elif evento.key == pygame.K_SPACE:
                    # Ativa a propulsão máxima
                    foguete.ativar_propulsao(intensidade=1.0)
                elif evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS:
                    # Aumenta o multiplicador de rotação do foguete
                    self.multiplicador_rotacao_foguete += 0.1
                elif evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                    # Diminui o multiplicador de rotação do foguete
                    self.multiplicador_rotacao_foguete = max(0.1, self.multiplicador_rotacao_foguete - 0.1)
                # Futuras teclas de menu podem ser adicionadas aqui
            elif evento.type == pygame.KEYUP:
                self.teclas_pressionadas.discard(evento.key)
                # Seção dos controles do foguete
                if evento.key == pygame.K_SPACE:
                    # Desativa a propulsão quando a tecla espaço é solta
                    foguete.desativar_propulsao()
        self.atualizar_controles(foguete)
        return True

    def atualizar_controles(self, foguete: Foguete) -> None:
        """
        Atualiza os controles contínuos, como a orientação do foguete e o movimento da câmera.
        """
        delta_orientacao = np.array([0.0, 0.0, 0.0])
        movimento_camera = np.array([0.0, 0.0, 0.0])
        rotacao_camera = np.array([0.0, 0.0, 0.0])

        # Controles do foguete
        velocidade_rotacao_foguete = 0.01 * self.multiplicador_rotacao_foguete

        if pygame.K_UP in self.teclas_pressionadas:
            # Inclina o foguete para cima
            delta_orientacao += np.array([0.0, 0.0, -velocidade_rotacao_foguete])
        if pygame.K_DOWN in self.teclas_pressionadas:
            # Inclina o foguete para baixo
            delta_orientacao += np.array([0.0, 0.0, velocidade_rotacao_foguete])
        if pygame.K_LEFT in self.teclas_pressionadas:
            # Inclina o foguete para a esquerda
            delta_orientacao += np.array([-velocidade_rotacao_foguete, 0.0, 0.0])
        if pygame.K_RIGHT in self.teclas_pressionadas:
            # Inclina o foguete para a direita
            delta_orientacao += np.array([velocidade_rotacao_foguete, 0.0, 0.0])

        if np.linalg.norm(delta_orientacao) > 0:
            foguete.atualizar_orientacao(delta_orientacao)

        # Controles da câmera - movimento
        velocidade_camera = 1e6  # Ajuste a velocidade conforme necessário

        if pygame.K_q in self.teclas_pressionadas:
            # Move a câmera para frente
            movimento_camera += np.array([0.0, 0.0, -velocidade_camera])
        if pygame.K_e in self.teclas_pressionadas:
            # Move a câmera para trás
            movimento_camera += np.array([0.0, 0.0, velocidade_camera])
        if pygame.K_w in self.teclas_pressionadas:
            # Move a câmera para a esquerda
            movimento_camera += np.array([-velocidade_camera, 0.0, 0.0])
        if pygame.K_s in self.teclas_pressionadas:
            # Move a câmera para a direita
            movimento_camera += np.array([velocidade_camera, 0.0, 0.0])
        if pygame.K_d in self.teclas_pressionadas:
            # Move a câmera para cima
            movimento_camera += np.array([0.0, velocidade_camera, 0.0])
        if pygame.K_a in self.teclas_pressionadas:
            # Move a câmera para baixo
            movimento_camera += np.array([0.0, -velocidade_camera, 0.0])

        # Controles da câmera - rotação
        velocidade_rotacao_camera = 0.5  # Velocidade de rotação da câmera em graus por frame

        if pygame.K_i in self.teclas_pressionadas:
            # Rotaciona a câmera para cima
            rotacao_camera += np.array([-velocidade_rotacao_camera, 0.0, 0.0])
        if pygame.K_k in self.teclas_pressionadas:
            # Rotaciona a câmera para baixo
            rotacao_camera += np.array([velocidade_rotacao_camera, 0.0, 0.0])
        if pygame.K_j in self.teclas_pressionadas:
            # Rotaciona a câmera para a esquerda
            rotacao_camera += np.array([0.0, -velocidade_rotacao_camera, 0.0])
        if pygame.K_l in self.teclas_pressionadas:
            # Rotaciona a câmera para a direita
            rotacao_camera += np.array([0.0, velocidade_rotacao_camera, 0.0])
        if pygame.K_o in self.teclas_pressionadas:
            # Rotaciona a câmera para a esquerda
            rotacao_camera += np.array([0.0, 0.0, -velocidade_rotacao_camera])
        if pygame.K_u in self.teclas_pressionadas:
            # Rotaciona a câmera para a direita
            rotacao_camera += np.array([0.0, 0.0, velocidade_rotacao_camera])

        self.movimento_camera = movimento_camera
        self.rotacao_camera = rotacao_camera

    def obter_movimento_camera(self) -> np.ndarray:
        """
        Retorna o vetor de movimento da câmera.

        :return: Vetor de movimento da câmera (np.ndarray).
        """
        return self.movimento_camera

    def obter_rotacao_camera(self) -> np.ndarray:
        """
        Retorna o vetor de rotação da câmera.

        :return: Vetor de rotação da câmera (np.ndarray).
        """
        return self.rotacao_camera

    def obter_vetor_up(self) -> np.ndarray:
        """
        Retorna o vetor "up" da câmera.

        :return: Vetor "up" da câmera (np.ndarray).
        """
        return self.vetor_up

    def obter_multiplicador_rotacao_foguete(self) -> float:
        """
        Retorna o multiplicador de rotação do foguete.

        :return: Multiplicador de rotação do foguete.
        """
        return self.multiplicador_rotacao_foguete
