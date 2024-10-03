import pygame
import numpy as np
from typing import List, Set
from simulacao.objetos.foguete import Foguete
from simulacao.grafico.camera import Camera
from simulacao.objetos.corpo_celeste import CorpoCeleste
from simulacao.controle.controlador import Controlador

class ManipuladorEntrada:
    """
    Classe responsável por gerenciar os inputs do usuário e atualizar os controles
    do foguete e da câmera na simulação.
    """
    def __init__(self):
        """
        Inicializa o manipulador de entrada com os estados iniciais.
        """
        self.teclas_pressionadas: Set[int] = set()
        self.simulacao_pausada: bool = False
        self.navegacao_automatica: bool = False
        self.controlador: Controlador = None

    def processar_eventos(self) -> bool:
        """
        Processa eventos do Pygame, atualizando o estado interno e respondendo a eventos chave.

        :param foguete: O objeto foguete controlado pelo usuário.
        :return: False se o usuário solicitar sair da simulação, True caso contrário.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                self._processar_tecla_pressionada(evento.key)
            elif evento.type == pygame.KEYUP:
                self._processar_tecla_solta(evento.key)
        return True

    def _processar_tecla_pressionada(self, tecla: int) -> None:
        """
        Processa eventos de teclas pressionadas.

        :param tecla: Código da tecla pressionada.
        :param foguete: O objeto foguete controlado pelo usuário.
        """
        self.teclas_pressionadas.add(tecla)

        # Controles gerais
        if tecla == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif tecla == pygame.K_m:
            self.simulacao_pausada = not self.simulacao_pausada
        # Futuras teclas de controle podem ser adicionadas aqui

    def _processar_tecla_solta(self, tecla: int) -> None:
        """
        Processa eventos de teclas soltas.

        :param tecla: Código da tecla solta.
        """
        self.teclas_pressionadas.discard(tecla)

    def _alternar_navegacao_automatica(self, foguete: Foguete) -> None:
        """
        Ativa ou desativa a navegação automática do foguete.

        :param foguete: O objeto foguete controlado.
        """
        self.navegacao_automatica = not self.navegacao_automatica
        if self.navegacao_automatica:
            # Inicializa o controlador para navegação automática
            self.controlador = Controlador(foguete)
        else:
            self.controlador = None
            foguete.desativar_propulsao()

    def atualizar_controles(self, foguete: Foguete, camera: Camera, delta_t: float) -> None:
        """
        Atualiza os controles contínuos, como a orientação do foguete e o movimento da câmera.

        :param foguete: O objeto foguete a ser controlado.
        :param camera: A câmera da simulação.
        :param delta_t: O tempo delta entre frames.
        """
        if self.navegacao_automatica and self.controlador:
            self.controlador.atualizar(delta_t)
        else:
            self._atualizar_controles_foguete(foguete)
        self._atualizar_controles_camera(camera)

    def _atualizar_controles_foguete(self, foguete: Foguete) -> None:
        """
        Atualiza a orientação e propulsão do foguete com base nas teclas pressionadas.

        :param foguete: O objeto foguete a ser controlado.
        """
        delta_orientacao = np.array([0.0, 0.0, 0.0])
        velocidade_rotacao_foguete = 1.0  # Velocidade de rotação em graus por frame

        # Controles de rotação do foguete
        if pygame.K_UP in self.teclas_pressionadas:
            delta_orientacao += np.array([-velocidade_rotacao_foguete, 0.0, 0.0])  # Pitch up
        if pygame.K_DOWN in self.teclas_pressionadas:
            delta_orientacao += np.array([velocidade_rotacao_foguete, 0.0, 0.0])   # Pitch down
        if pygame.K_LEFT in self.teclas_pressionadas:
            delta_orientacao += np.array([0.0, -velocidade_rotacao_foguete, 0.0])  # Yaw left
        if pygame.K_RIGHT in self.teclas_pressionadas:
            delta_orientacao += np.array([0.0, velocidade_rotacao_foguete, 0.0])   # Yaw right
        if pygame.K_z in self.teclas_pressionadas:
            delta_orientacao += np.array([0.0, 0.0, velocidade_rotacao_foguete])   # Roll clockwise
        if pygame.K_x in self.teclas_pressionadas:
            delta_orientacao += np.array([0.0, 0.0, -velocidade_rotacao_foguete])  # Roll counter-clockwise

        if np.linalg.norm(delta_orientacao) > 0:
            foguete.atualizar_orientacao(delta_orientacao)

        # Propulsão
        if pygame.K_SPACE in self.teclas_pressionadas:
            foguete.ativar_propulsao(intensidade=1.0)
        else:
            foguete.desativar_propulsao()
        if pygame.K_n in self.teclas_pressionadas:
            self._alternar_navegacao_automatica(foguete)

    def _atualizar_controles_camera(self, camera: Camera) -> None:
        """
        Atualiza a posição e rotação da câmera com base nas teclas pressionadas.

        :param camera: A câmera da simulação.
        """
        movimento_camera = np.array([0.0, 0.0, 0.0])
        rotacao_camera = np.array([0.0, 0.0, 0.0])

        velocidade_camera = 1e9  # Velocidade de movimento da câmera
        velocidade_rotacao_camera = 0.5  # Velocidade de rotação da câmera em graus por frame

        # Movimento da câmera
        if pygame.K_w in self.teclas_pressionadas:
            movimento_camera += np.array([-velocidade_camera, 0.0, 0.0])  # Move forward
        if pygame.K_s in self.teclas_pressionadas:
            movimento_camera += np.array([velocidade_camera, 0.0, 0.0])   # Move backward
        if pygame.K_a in self.teclas_pressionadas:
            movimento_camera += np.array([0.0, velocidade_camera, 0.0])  # Move left
        if pygame.K_d in self.teclas_pressionadas:
            movimento_camera += np.array([0.0, -velocidade_camera, 0.0])   # Move right
        if pygame.K_q in self.teclas_pressionadas:
            movimento_camera += np.array([0.0, 0.0, -velocidade_camera])   # Move up
        if pygame.K_e in self.teclas_pressionadas:
            movimento_camera += np.array([0.0, 0.0, velocidade_camera])  # Move down

        # Rotação da câmera
        if pygame.K_i in self.teclas_pressionadas:
            rotacao_camera += np.array([-velocidade_rotacao_camera, 0.0, 0.0])  # Pitch up
        if pygame.K_k in self.teclas_pressionadas:
            rotacao_camera += np.array([velocidade_rotacao_camera, 0.0, 0.0])   # Pitch down
        if pygame.K_j in self.teclas_pressionadas:
            rotacao_camera += np.array([0.0, -velocidade_rotacao_camera, 0.0])  # Yaw left
        if pygame.K_l in self.teclas_pressionadas:
            rotacao_camera += np.array([0.0, velocidade_rotacao_camera, 0.0])   # Yaw right
        if pygame.K_u in self.teclas_pressionadas:
            rotacao_camera += np.array([0.0, 0.0, velocidade_rotacao_camera])   # Roll clockwise
        if pygame.K_o in self.teclas_pressionadas:
            rotacao_camera += np.array([0.0, 0.0, -velocidade_rotacao_camera])  # Roll counter-clockwise

        # Atualiza a câmera
        if np.linalg.norm(movimento_camera) > 0:
            camera.mover_camera_relativo(movimento_camera)
        if np.linalg.norm(rotacao_camera) > 0:
            camera.rotacao += rotacao_camera

    def esta_pausado(self) -> bool:
        """
        Verifica se a simulação está pausada.

        :return: True se a simulação estiver pausada, False caso contrário.
        """
        return self.simulacao_pausada
