import pygame
import numpy as np
from simulacao.objetos.foguete import Foguete
from simulacao.grafico.camera import Camera

class ManipuladorEntrada:
    """
    Classe responsável por gerenciar os inputs do usuário.
    """
    def __init__(self):
        self.teclas_pressionadas = set()
        self.movimento_camera = np.array([0.0, 0.0, 0.0])
        self.rotacao_camera = np.array([0.0, 0.0, 0.0])  # Rotação em torno dos eixos X, Y, Z
        self.simulacao_pausada = False

    def processar_eventos(self, foguete: Foguete, camera: Camera) -> bool:
        """
        Processa eventos do pygame e aplica movimentos à câmera e ao foguete.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                self.teclas_pressionadas.add(evento.key)
                if evento.key == pygame.K_ESCAPE:
                    return False
                elif evento.key == pygame.K_m:
                    # Alterna o estado de pausa
                    self.simulacao_pausada = not self.simulacao_pausada
            elif evento.type == pygame.KEYUP:
                self.teclas_pressionadas.discard(evento.key)

        self.atualizar_controles(foguete, camera)
        return True

    def atualizar_controles(self, foguete: Foguete, camera: Camera) -> None:
        """
        Atualiza os controles contínuos, como a orientação do foguete e o movimento da câmera.
        """
        delta_orientacao = np.array([0.0, 0.0, 0.0])
        movimento_camera = np.array([0.0, 0.0, 0.0])
        rotacao_camera = np.array([0.0, 0.0, 0.0])  # Para acumular as rotações da câmera

        # Controles do foguete
        velocidade_rotacao_foguete = 1.0

        if pygame.K_UP in self.teclas_pressionadas:
            delta_orientacao += np.array([0.0, 0.0, -velocidade_rotacao_foguete])
        if pygame.K_DOWN in self.teclas_pressionadas:
            delta_orientacao += np.array([0.0, 0.0, velocidade_rotacao_foguete])
        if pygame.K_LEFT in self.teclas_pressionadas:
            delta_orientacao += np.array([-velocidade_rotacao_foguete, 0.0, 0.0])
        if pygame.K_RIGHT in self.teclas_pressionadas:
            delta_orientacao += np.array([velocidade_rotacao_foguete, 0.0, 0.0])
        if pygame.K_z in self.teclas_pressionadas:
            delta_orientacao += np.array([0.0, -velocidade_rotacao_foguete, 0.0])
        if pygame.K_x in self.teclas_pressionadas:
            delta_orientacao += np.array([0.0, velocidade_rotacao_foguete, 0.0])

        if np.linalg.norm(delta_orientacao) > 0:
            foguete.atualizar_orientacao(delta_orientacao)

        # Controles da câmera (relativo à sua orientação)
        velocidade_camera = 1e9  # Ajuste a velocidade conforme necessário

        if pygame.K_w in self.teclas_pressionadas:
            movimento_camera += np.array([-velocidade_camera,0.0, 0.0])  # Frente
        if pygame.K_s in self.teclas_pressionadas:
            movimento_camera += np.array([velocidade_camera,0.0, 0.0])   # Trás
        if pygame.K_a in self.teclas_pressionadas:
            movimento_camera += np.array([0.0, velocidade_camera, 0.0])  # Esquerda
        if pygame.K_d in self.teclas_pressionadas:
            movimento_camera += np.array([0.0, -velocidade_camera, 0.0])   # Direita
        if pygame.K_q in self.teclas_pressionadas:
            movimento_camera += np.array([0.0, 0.0, -velocidade_camera])   # Cima
        if pygame.K_e in self.teclas_pressionadas:
            movimento_camera += np.array([0.0, 0.0, velocidade_camera])  # Baixo

        # Controles de rotação da câmera com as teclas 'u', 'i', 'o', 'j', 'k', 'l'
        velocidade_rotacao_camera = 0.5  # Velocidade de rotação da câmera em graus por frame

        if pygame.K_i in self.teclas_pressionadas:
            rotacao_camera += np.array([-velocidade_rotacao_camera, 0.0, 0.0])  # Rotaciona para cima
        if pygame.K_k in self.teclas_pressionadas:
            rotacao_camera += np.array([velocidade_rotacao_camera, 0.0, 0.0])   # Rotaciona para baixo
        if pygame.K_j in self.teclas_pressionadas:
            rotacao_camera += np.array([0.0, -velocidade_rotacao_camera, 0.0])  # Rotaciona para a esquerda
        if pygame.K_l in self.teclas_pressionadas:
            rotacao_camera += np.array([0.0, velocidade_rotacao_camera, 0.0])   # Rotaciona para a direita
        if pygame.K_u in self.teclas_pressionadas:
            rotacao_camera += np.array([0.0, 0.0, velocidade_rotacao_camera])  # Rotaciona em torno do eixo Z (anti-horário)
        if pygame.K_o in self.teclas_pressionadas:
            rotacao_camera += np.array([0.0, 0.0, -velocidade_rotacao_camera])   # Rotaciona em torno do eixo Z (horário)

        # Aplica a rotação acumulada à câmera
        camera.rotacao += rotacao_camera

        # Atualiza o movimento da câmera com base na sua posição e rotação atuais
        camera.mover_camera_relativo(movimento_camera)

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

    def esta_pausado(self) -> bool:
        """
        Retorna o estado de pausa da simulação.

        :return: True se a simulação estiver pausada, False caso contrário.
        """
        return self.simulacao_pausada
