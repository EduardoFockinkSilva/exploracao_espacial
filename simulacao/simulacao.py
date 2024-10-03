# simulacao/simulacao.py

import pygame
import numpy as np
from simulacao.grafico.motor_grafico import MotorGrafico
from simulacao.grafico.camera import Camera
from simulacao.fisica.motor_fisico import MotorFisico
from simulacao.controle.manipulador_entrada import ManipuladorEntrada
from simulacao.controle.controlador import Controlador
from simulacao.objetos.corpo_celeste import CorpoCeleste
from simulacao.objetos.foguete import Foguete
from simulacao.util.gerenciador_dados import carregar_dados_json, criar_corpos_celestes, criar_foguete

class Simulacao:
    def __init__(self):
        # Inicializa o Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 60  # Frames por segundo
        self.delta_t = 3600.0  # Tempo entre frames

        # Inicializa os componentes principais
        self.motor_grafico = MotorGrafico(largura=1200, altura=920)
        self.camera = Camera(
            posicao=np.array([6e11, 0, 5e10]),
            alvo=np.array([0.0, 0.0, 0.0]),
            rotacao=np.array([0.0, 0.0, -90.0])
        )
        self.motor_fisico = MotorFisico()
        self.manipulador_entrada = ManipuladorEntrada()
        self.controlador = None  # Será inicializado se a navegação automática for ativada

        # Carrega os dados da cena
        self.corpos = []
        self.foguete = None
        self.carregar_cena("simulacao/cenas/solar.json")

        # Estado da simulação
        self.executando = True
        self.simulacao_pausada = False

    def carregar_cena(self, caminho_arquivo: str):
        # Carrega os dados dos corpos celestes e foguete a partir do JSON
        dados = carregar_dados_json(caminho_arquivo)

        # Cria os corpos celestes
        self.corpos = criar_corpos_celestes(dados["corpos"])

        # Cria o foguete
        terra = next(corpo for corpo in self.corpos if corpo.nome == "Terra")
        self.foguete = criar_foguete(dados["foguete"], terra)

        # Adiciona o foguete à lista de corpos
        self.corpos.append(self.foguete)

    def executar(self):
        while self.executando:
            # Processa eventos
            self.executando = self.manipulador_entrada.processar_eventos(
                self.foguete, self.camera, self.corpos
            )

            # Atualiza os controles
            self.manipulador_entrada.atualizar_controles(
                self.foguete, self.camera, self.delta_t
            )

            # Verifica se a simulação está pausada
            self.simulacao_pausada = self.manipulador_entrada.esta_pausado()

            # Atualiza a física somente se a simulação não estiver pausada
            if not self.simulacao_pausada:
                self.motor_fisico.atualizar_corpos(self.corpos, self.delta_t)
                self.foguete.atualizar_estado(self.delta_t)

            # Limpa a tela
            self.motor_grafico.limpar_tela()

            # Ajusta a câmera
            #self.camera.atualizar()
            self.camera.ajustar_camera()

            # Desenha os corpos celestes
            self.motor_grafico.desenhar_corpos(self.corpos)

            # Atualiza a tela
            self.motor_grafico.atualizar_tela()

            # Atualiza o relógio
            self.clock.tick(self.fps)

        # Encerra o Pygame
        pygame.quit()
