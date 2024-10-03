from simulacao.objetos.corpo_celeste import CorpoCeleste
from typing import Tuple
import numpy as np

class Foguete(CorpoCeleste):
    """
    Classe que representa um foguete na simulação.
    Herda de CorpoCeleste e adiciona funcionalidades específicas de propulsão.
    """
    def __init__(
        self,
        nome: str,
        massa: float,
        raio: float,
        cor: Tuple[int, int, int],
        fator_escala: float = 1.0,
        posicao: np.ndarray = None,
        velocidade: np.ndarray = None,
        orientacao: np.ndarray = None,
        empuxo_maximo: float = 0.0,
        consumo_combustivel: float = 0.0,
        combustivel_inicial: float = 0.0,
        max_rastro: int = 1000,
    ):
        """
        Inicializa um novo foguete.

        :param nome: Nome do foguete.
        :param massa: Massa total inicial (incluindo combustível) em kg.
        :param raio: Raio para representação gráfica.
        :param cor: Cor RGB para representação gráfica.
        :param fator_escala: Fator de escala para visualização.
        :param posicao: Vetor posição inicial (np.ndarray).
        :param velocidade: Vetor velocidade inicial (np.ndarray).
        :param orientacao: Vetor direção inicial do foguete (np.ndarray).
        :param empuxo_maximo: Empuxo máximo do motor em Newtons.
        :param consumo_combustivel: Taxa de consumo de combustível em kg/s.
        :param combustivel_inicial: Quantidade inicial de combustível em kg.
        :param max_rastro: Número máximo de pontos no rastro.
        """
        super().__init__(
            nome=nome,
            massa=massa,
            raio=raio,
            cor=cor,
            fator_escala=fator_escala,
            posicao=posicao,
            velocidade=velocidade,
            max_rastro=max_rastro,
        )
        self.orientacao = orientacao if orientacao is not None else np.array([0.0, 1.0, 0.0])
        self.empuxo_maximo = empuxo_maximo
        self.consumo_combustivel = consumo_combustivel
        self.combustivel_restante = combustivel_inicial
        self.aceleracao_propulsao = np.zeros(3)
        self.propulsao_ativa = False

    def ativar_propulsao(self, intensidade: float) -> None:
        """
        Ativa a propulsão do foguete.

        :param intensidade: Intensidade do empuxo (entre 0 e 1).
        """
        if self.combustivel_restante > 0:
            empuxo = self.empuxo_maximo * intensidade
            vetor_direcao = self.calcular_vetor_direcao()
            self.aceleracao_propulsao = (empuxo / self.massa) * vetor_direcao
            self.propulsao_ativa = True
        else:
            self.aceleracao_propulsao = np.zeros(3)
            self.propulsao_ativa = False


    def desativar_propulsao(self) -> None:
        """
        Desativa a propulsão do foguete.
        """
        self.aceleracao_propulsao = np.zeros(3)
        self.propulsao_ativa = False

    def calcular_vetor_direcao(self) -> np.ndarray:
        """
        Calcula o vetor de direção do foguete com base em seus ângulos de orientação.
        
        :return: Vetor de direção (np.ndarray).
        """
        pitch_rad = np.radians(self.orientacao[0])
        yaw_rad = np.radians(self.orientacao[1])
        roll_rad = np.radians(self.orientacao[2])

        # Cálculo do vetor de direção usando os ângulos de Euler
        # Aqui, consideramos que o foguete aponta inicialmente no eixo Z positivo
        # e aplicamos as rotações na ordem: roll, pitch, yaw
        # Você pode ajustar conforme o sistema de coordenadas do seu OpenGL

        # Matriz de rotação para pitch (X)
        rot_x = np.array([
            [1, 0, 0],
            [0, np.cos(pitch_rad), -np.sin(pitch_rad)],
            [0, np.sin(pitch_rad), np.cos(pitch_rad)]
        ])

        # Matriz de rotação para yaw (Y)
        rot_y = np.array([
            [np.cos(yaw_rad), 0, np.sin(yaw_rad)],
            [0, 1, 0],
            [-np.sin(yaw_rad), 0, np.cos(yaw_rad)]
        ])

        # Matriz de rotação para roll (Z)
        rot_z = np.array([
            [np.cos(roll_rad), -np.sin(roll_rad), 0],
            [np.sin(roll_rad), np.cos(roll_rad), 0],
            [0, 0, 1]
        ])

        # Matriz de rotação total
        rotacao_total = rot_z @ rot_y @ rot_x

        # Vetor de direção inicial (eixo Z positivo)
        direcao_inicial = np.array([0.0, 0.0, 1.0])

        # Aplica a rotação ao vetor de direção
        vetor_direcao = rotacao_total @ direcao_inicial

        return vetor_direcao

    def atualizar_orientacao(self, delta_orientacao: np.ndarray) -> None:
        """
        Atualiza a orientação do foguete.

        :param delta_orientacao: Vetor de rotação a ser aplicado à orientação atual (em graus).
        """
        self.orientacao += delta_orientacao
        # Opcionalmente, podemos limitar os ângulos entre 0 e 360 graus
        self.orientacao = np.mod(self.orientacao, 360)


    def atualizar_estado(self, delta_t: float) -> None:
        """
        Atualiza o estado do foguete, incluindo consumo de combustível.

        :param delta_t: Intervalo de tempo em segundos.
        """
        if self.propulsao_ativa and self.combustivel_restante > 0:
            consumo = self.consumo_combustivel * delta_t
            if consumo > self.combustivel_restante:
                consumo = self.combustivel_restante
                self.desativar_propulsao()
            self.combustivel_restante -= consumo
            # Atualiza a massa do foguete (massa total diminui)
            self.massa -= consumo
        else:
            self.aceleracao_propulsao = np.zeros(3)
            self.propulsao_ativa = False

    def calcular_forca_propulsao(self) -> np.ndarray:
        """
        Retorna a força de propulsão atual.

        :return: Vetor de força de propulsão (np.ndarray).
        """
        return self.aceleracao_propulsao * self.massa

    def atualizar_velocidade(self, aceleracao_total: np.ndarray, delta_t: float) -> None:
        """
        Atualiza a velocidade do foguete com base na aceleração total.

        :param aceleracao_total: Vetor de aceleração total (np.ndarray).
        :param delta_t: Intervalo de tempo em segundos.
        """
        self.velocidade += aceleracao_total * delta_t

    def atualizar_posicao(self, delta_t: float) -> None:
        """
        Atualiza a posição do foguete com base em sua velocidade atual.

        :param delta_t: Intervalo de tempo em segundos.
        """
        super().atualizar_posicao(delta_t)
