import pygame
import numpy as np
from simulacao.grafico.motor_grafico import MotorGrafico
from simulacao.grafico.camera import Camera
from simulacao.fisica.motor_fisico import MotorFisico
from simulacao.controle.manipulador_entrada import ManipuladorEntrada
from simulacao.objetos.corpo_celeste import CorpoCeleste
from simulacao.objetos.foguete import Foguete
from simulacao.util.gerenciador_dados import carregar_dados_json, criar_corpos_celestes, criar_foguete

class Simulacao:
    """
    Classe principal que gerencia a execução da simulação.
    """
    def __init__(self):
        """
        Inicializa a simulação, carregando os componentes necessários.
        """
        # Inicializa o Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 60  # Frames por segundo

        # Tempo de simulação (pode ser escalado para acelerar ou desacelerar o tempo na simulação)
        self.delta_t = 3600.0 * self.fps  # Em segundos (1 hora por frame)

        # Inicializa os componentes principais
        self.motor_grafico = MotorGrafico(largura=1200, altura=920)
        self.camera = Camera(
            posicao=np.array([3e11, 0, 5e10]),
            alvo=np.array([0.0, 0.0, 0.0]),
            rotacao=np.array([0.0, 0.0, -90.0])
        )
        self.motor_fisico = MotorFisico()
        self.manipulador_entrada = ManipuladorEntrada()

        # Carrega os dados da cena
        self.corpos = []
        self.foguete = None
        self.carregar_cena("simulacao/cenas/solar.json")

        # Estado da simulação
        self.executando = True

    def carregar_cena(self, caminho_arquivo: str):
        """
        Carrega os dados dos corpos celestes e do foguete a partir de um arquivo JSON.

        :param caminho_arquivo: Caminho para o arquivo JSON da cena.
        """
        dados = carregar_dados_json(caminho_arquivo)

        # Cria os corpos celestes
        self.corpos = criar_corpos_celestes(dados["corpos"])

        # Cria o foguete e o adiciona aos corpos
        terra = next(corpo for corpo in self.corpos if corpo.nome == "Terra")
        marte = next(corpo for corpo in self.corpos if corpo.nome == "Marte")
        self.foguete = criar_foguete(dados["foguete"], terra, marte)
        self.corpos.append(self.foguete)

    def executar(self):
        """
        Método principal que executa o loop da simulação.
        """
        while self.executando:
            # Processa eventos
            self.executando = self.manipulador_entrada.processar_eventos()

            # Calcula o delta_t real entre frames (em segundos)
            delta_t_frame = self.clock.get_time() / 1000.0  # Converte de milissegundos para segundos
            delta_t_simulacao = delta_t_frame * self.delta_t  # Escala o tempo de simulação

            # Atualiza os controles
            self.manipulador_entrada.atualizar_controles(
                self.foguete, self.camera, delta_t_frame
            )

            # Verifica se a simulação está pausada
            if not self.manipulador_entrada.esta_pausado():
                # Atualiza a física dos corpos
                self.motor_fisico.atualizar_corpos(self.corpos, delta_t_simulacao)

            # Limpa a tela
            self.motor_grafico.limpar_tela()

            # Atualiza a câmera
            self.camera.atualizar()

            # Desenha os corpos celestes
            self.motor_grafico.desenhar_corpos(self.corpos)

            # Atualiza a tela
            self.motor_grafico.atualizar_tela()

            # Atualiza o relógio
            self.clock.tick(self.fps)  # Mantém a taxa de quadros desejada

        # Encerra o Pygame ao sair do loop
        pygame.quit()
