import numpy as np
from simulacao.objetos.foguete import Foguete
from simulacao.objetos.corpo_celeste import CorpoCeleste
from typing import List, Tuple
import time

class Nodo:
    def __init__(self, posicao: np.ndarray, g: float, h: float, f: float, pai=None):
        self.posicao = posicao
        self.g = g  # Custo do caminho desde o início até este nodo
        self.h = h  # Heurística (estimativa do custo até o objetivo)
        self.f = f  # f = g + h
        self.pai = pai

class Navegador:
    def __init__(self, foguete: Foguete, destino: CorpoCeleste):
        self.foguete = foguete
        self.destino = destino
        self.caminho: List[Nodo] = []
        self.indice_acao_atual = 0
        self.resolucao = 1e9  # Tamanho das células da grade
        self.raio_planejamento = 1e10  # Raio para o planejamento incremental
        self.tempo_maximo_planejamento = 0.1  # Tempo máximo (em segundos) para o planejamento em cada iteração

    def calcular_caminho_incremental(self):
        """
        Executa o algoritmo A* para encontrar o caminho até um ponto intermediário.
        """
        inicio = self.foguete.posicao
        objetivo = self.destino.posicao

        # Verifica se já está próximo o suficiente do destino
        if np.linalg.norm(objetivo - inicio) < self.resolucao:
            self.caminho = []
            return

        # Define o ponto intermediário como sendo dentro do raio de planejamento
        direcao_ao_destino = objetivo - inicio
        distancia_ao_destino = np.linalg.norm(direcao_ao_destino)
        direcao_ao_destino_normalizada = direcao_ao_destino / distancia_ao_destino

        if distancia_ao_destino > self.raio_planejamento:
            objetivo_intermediario = inicio + direcao_ao_destino_normalizada * self.raio_planejamento
        else:
            objetivo_intermediario = objetivo

        # Cria o nodo inicial e o objetivo intermediário
        nodo_inicial = Nodo(posicao=inicio, g=0, h=0, f=0)
        nodo_objetivo = Nodo(posicao=objetivo_intermediario, g=0, h=0, f=0)

        # Listas de nodos abertos e fechados
        lista_aberta: List[Nodo] = []
        lista_fechada: List[Nodo] = []

        lista_aberta.append(nodo_inicial)

        inicio_tempo = time.time()

        while lista_aberta:
            # Verifica se o tempo máximo de planejamento foi excedido
            if time.time() - inicio_tempo > self.tempo_maximo_planejamento:
                break

            # Seleciona o nodo com o menor f
            nodo_atual = min(lista_aberta, key=lambda n: n.f)
            lista_aberta.remove(nodo_atual)
            lista_fechada.append(nodo_atual)

            # Verifica se chegou ao objetivo intermediário (com uma tolerância)
            if np.linalg.norm(nodo_atual.posicao - nodo_objetivo.posicao) < self.resolucao:
                # Reconstrói o caminho
                caminho = []
                atual = nodo_atual
                while atual is not None:
                    caminho.append(atual)
                    atual = atual.pai
                self.caminho = caminho[::-1]  # Inverte o caminho
                return

            # Gera os nodos vizinhos
            vizinhos = self.get_vizinhos(nodo_atual)

            for vizinho_pos in vizinhos:
                # Verifica se o vizinho já está na lista fechada
                if any(np.array_equal(vizinho_pos, n.posicao) for n in lista_fechada):
                    continue

                # Calcula g, h e f
                g = nodo_atual.g + self.custo_movimento(nodo_atual.posicao, vizinho_pos)
                h = self.heuristica(vizinho_pos, nodo_objetivo.posicao)
                f = g + h

                # Verifica se o vizinho já está na lista aberta com um custo menor
                nodo_vizinho = next((n for n in lista_aberta if np.array_equal(vizinho_pos, n.posicao)), None)
                if nodo_vizinho and g >= nodo_vizinho.g:
                    continue

                if nodo_vizinho is None:
                    nodo_vizinho = Nodo(posicao=vizinho_pos, g=g, h=h, f=f, pai=nodo_atual)
                    lista_aberta.append(nodo_vizinho)
                else:
                    nodo_vizinho.g = g
                    nodo_vizinho.h = h
                    nodo_vizinho.f = f
                    nodo_vizinho.pai = nodo_atual

        # Se não encontrou um caminho dentro do tempo limite, utiliza o melhor nodo encontrado
        if lista_fechada:
            nodo_atual = min(lista_fechada, key=lambda n: n.h)
            caminho = []
            atual = nodo_atual
            while atual is not None:
                caminho.append(atual)
                atual = atual.pai
            self.caminho = caminho[::-1]
        else:
            self.caminho = []

    def get_vizinhos(self, nodo: Nodo) -> List[np.ndarray]:
        """
        Retorna os vizinhos de um nodo na grade.
        """
        movimentos = [
            np.array([self.resolucao, 0, 0]),
            np.array([-self.resolucao, 0, 0]),
            np.array([0, self.resolucao, 0]),
            np.array([0, -self.resolucao, 0]),
            np.array([0, 0, self.resolucao]),
            np.array([0, 0, -self.resolucao]),
        ]
        vizinhos = [nodo.posicao + movimento for movimento in movimentos]
        return vizinhos

    def custo_movimento(self, pos_atual: np.ndarray, pos_vizinho: np.ndarray) -> float:
        """
        Calcula o custo de mover-se de uma posição para outra.
        """
        return np.linalg.norm(pos_vizinho - pos_atual)

    def heuristica(self, posicao: np.ndarray, objetivo: np.ndarray) -> float:
        """
        Calcula a heurística (distância Euclidiana) até o objetivo.
        """
        return np.linalg.norm(objetivo - posicao)

    def executar_proxima_acao(self):
        """
        Executa a próxima ação planejada pelo caminho.
        """
        if not self.caminho or self.indice_acao_atual >= len(self.caminho):
            # Recalcula o caminho incremental
            self.calcular_caminho_incremental()
            self.indice_acao_atual = 0

            if not self.caminho:
                # Não encontrou caminho, desativa a propulsão
                self.foguete.desativar_propulsao()
                return

        nodo_destino = self.caminho[self.indice_acao_atual]
        direcao_desejada = nodo_destino.posicao - self.foguete.posicao
        distancia = np.linalg.norm(direcao_desejada)

        if distancia < self.resolucao:
            self.indice_acao_atual += 1
            return

        direcao_desejada_normalizada = direcao_desejada / distancia

        # Calcula a diferença entre a orientação atual e a desejada
        vetor_direcao_atual = self.foguete.calcular_vetor_direcao()
        angulo_diferenca = np.arccos(np.clip(np.dot(vetor_direcao_atual, direcao_desejada_normalizada), -1.0, 1.0))

        # Se a diferença de ângulo for pequena, ativa a propulsão
        if angulo_diferenca < np.radians(5):
            self.foguete.ativar_propulsao(intensidade=1.0)
        else:
            # Rotaciona o foguete na direção correta
            eixo_rotacao = np.cross(vetor_direcao_atual, direcao_desejada_normalizada)
            if np.linalg.norm(eixo_rotacao) > 0:
                eixo_rotacao_normalizado = eixo_rotacao / np.linalg.norm(eixo_rotacao)
                delta_orientacao = eixo_rotacao_normalizado * np.degrees(0.1)  # Ajuste o fator conforme necessário
                self.foguete.atualizar_orientacao(delta_orientacao)
            else:
                # Orientação já alinhada, não faz nada
                pass

        # Verifica se chegou ao nodo destino
        if distancia < self.resolucao:
            self.indice_acao_atual += 1  # Avança para o próximo nodo
