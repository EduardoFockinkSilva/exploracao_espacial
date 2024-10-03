import numpy as np
from simulacao.objetos.foguete import Foguete
from simulacao.objetos.corpo_celeste import CorpoCeleste

class Controlador:
    def __init__(self, foguete: Foguete):
        self.foguete = foguete
        self.destino = self.foguete.destino
        self.kp_posicao = 1e-4  # Ganho proporcional para posição
        self.kp_velocidade = 1e-2  # Ganho proporcional para velocidade

    def atualizar(self, delta_t: float):
        # Calcula o erro de posição
        erro_posicao = self.destino.posicao - self.foguete.posicao

        # Calcula a velocidade desejada
        velocidade_desejada = erro_posicao * self.kp_posicao

        # Calcula o erro de velocidade
        erro_velocidade = velocidade_desejada - self.foguete.velocidade

        # Calcula a aceleração desejada
        aceleracao_desejada = erro_velocidade * self.kp_velocidade

        # Limita a aceleração máxima do foguete
        aceleracao_maxima = self.foguete.empuxo_maximo / self.foguete.massa
        if np.linalg.norm(aceleracao_desejada) > aceleracao_maxima:
            aceleracao_desejada = aceleracao_desejada / np.linalg.norm(aceleracao_desejada) * aceleracao_maxima

        # Calcula a orientação desejada
        if np.linalg.norm(aceleracao_desejada) > 0:
            direcao_desejada = aceleracao_desejada / np.linalg.norm(aceleracao_desejada)
        else:
            direcao_desejada = self.foguete.calcular_vetor_direcao()

        # Ajusta a orientação do foguete
        self.ajustar_orientacao_foguete(direcao_desejada, delta_t)

        # Ativa a propulsão com intensidade proporcional à aceleração desejada
        intensidade_propulsao = np.linalg.norm(aceleracao_desejada) / aceleracao_maxima
        self.foguete.ativar_propulsao(intensidade=intensidade_propulsao)

    def ajustar_orientacao_foguete(self, direcao_desejada: np.ndarray, delta_t: float):
        # Calcula a diferença entre a orientação atual e a desejada
        vetor_direcao_atual = self.foguete.calcular_vetor_direcao()
        angulo_diferenca = np.arccos(np.clip(np.dot(vetor_direcao_atual, direcao_desejada), -1.0, 1.0))

        # Calcula o eixo de rotação
        eixo_rotacao = np.cross(vetor_direcao_atual, direcao_desejada)
        if np.linalg.norm(eixo_rotacao) > 0:
            eixo_rotacao_normalizado = eixo_rotacao / np.linalg.norm(eixo_rotacao)
        else:
            eixo_rotacao_normalizado = np.zeros(3)

        # Define a velocidade de rotação
        velocidade_rotacao = 1.0  # graus por segundo
        delta_orientacao = eixo_rotacao_normalizado * velocidade_rotacao * delta_t

        # Atualiza a orientação do foguete
        self.foguete.atualizar_orientacao(delta_orientacao)
