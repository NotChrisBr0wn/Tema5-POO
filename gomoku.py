# gomoku.py (template)
"""
Template para implementar o jogo Gomoku (Cinco em Linha).
Deve implementar todos os métodos abstratos herdados de Jogo.
"""

import pickle
from jogo_abs import Jogo
from random import randint


class Gomoku(Jogo):
    """
    Classe concreta que herda da classe Jogo e implementa o jogo Gomoku.
    """

    def inicializa_tabuleiro(self) -> None:
        """
        Inicializa o tabuleiro 10x10 com espaços vazios ' '.
        """
        self.tabuleiro = [[' ' for _ in range(10)] for _ in range(10)]

    def mostra_tabuleiro(self) -> None:
        """
        Desenha o tabuleiro na consola.
        Dica: Pode usar enumerate() para numerar as linhas.
        """
        print()
        cabecalho = "  | " + " | ".join(str(c) for c in range(10)) + " |"
        print(cabecalho)
        for i, linha in enumerate(self.tabuleiro):
            conteudo_linha = " | ".join(linha)
            print(f"{i} | {conteudo_linha} |")
        print()

    def joga_humano(self, jogador: int) -> None:
        """
        Pede ao jogador humano as coordenadas (linha, coluna) da jogada
        e coloca a peça no tabuleiro.
        - Jogador 0 usa 'O', Jogador 1 usa 'X'.
        - Deve validar se a posição está dentro do tabuleiro e está livre.
        :param jogador: número do jogador (0 ou 1).
        """
        peca = 'O' if jogador == 0 else 'X'
        
        while True:
            try:
                coords = input(f"Jogador {jogador} ({peca}), introduza linha coluna (0-9), 's' para guardar ou 'c' para carregar: ")

                if coords.strip().lower() == 's':
                    self.guardar_estado()
                    continue
                if coords.strip().lower() == 'c':
                    self.carregar_estado()
                    self.mostra_tabuleiro()
                    continue

                linha, coluna = map(int, coords.split())
                
                # Verifica se a posição está dentro do tabuleiro
                if linha < 0 or linha > 9 or coluna < 0 or coluna > 9:
                    print("Posição fora do tabuleiro! Tente novamente.")
                    continue
                
                # Verificar se está vazio
                if self.tabuleiro[linha][coluna] != ' ':
                    print("❌ Posição ocupada! Tente novamente.")
                    continue
                
                # Colocar a peça
                self.tabuleiro[linha][coluna] = peca
                break
            except (ValueError, IndexError):
                print("⚠️ Entrada inválida! Use o formato: linha coluna")
                continue

    def n_linha(self, peca: str, n: int) -> bool:
        """Verifica se a peça dada tem n ou mais peças seguidas em qualquer direção."""
        direcoes = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for linha in range(10):
            for coluna in range(10):
                if self.tabuleiro[linha][coluna] == peca:
                    for dx, dy in direcoes:
                        contador = 1
                        x, y = linha + dx, coluna + dy
                        while 0 <= x < 10 and 0 <= y < 10 and self.tabuleiro[x][y] == peca:
                            contador += 1
                            x += dx
                            y += dy
                        if contador >= n:
                            return True
        return False

    def maximo_linha (self, linha: int, coluna: int, peca: str) -> int:
        # Conta o numero maximo de pecas iguais em linha
        direcoes = [(0, 1), (1, 0), (1, 1), (1, -1)]
        melhor = 1

        for dx, dy in direcoes:
            contador = 1

            x, y = linha + dx, coluna + dy
            while 0 <= x < 10 and 0 <= y < 10 and self.tabuleiro[x][y] == peca:
                contador += 1
                x += dx
                y += dy
                
            x, y = linha - dx, coluna - dy
            while 0 <= x < 10 and 0 <= y < 10 and self.tabuleiro[x][y] == peca:
                contador += 1
                x -= dx
                y -= dy

            if contador > melhor:
                melhor = contador

        return melhor

    def jogada_prioritaria(self, peca: str, n: int):
        # Procura uma jogada que crie 3/4/5 em linha, senao bloqueia o adversário
        for linha in range(10):
            for coluna in range(10):
                if self.tabuleiro[linha][coluna] == ' ':
                    self.tabuleiro[linha][coluna] = peca
                    vencedora = self.maximo_linha (linha, coluna, peca) >= n
                    self.tabuleiro[linha][coluna] = ' '
                    if vencedora:
                        return (linha, coluna)
        return None

    def joga_computador(self, jogador: int) -> None:
        """
        Realiza uma jogada aleatória do computador numa posição livre.(Agora inteligente)
        !Realiza uma jogada inteligente do computador:
        - Tenta vencer imediatamente.
        - Bloqueia vitória imediata do adversário.
        -  Caso contrário, joga aleatoriamente.

        - Jogador 0 usa 'O', Jogador 1 usa 'X'.
        :para jogador: número do jogador (computador).
        """
        peca = 'O' if jogador == 0 else 'X'
        adversario = 'X' if peca == 'O' else 'O'

        # Tentar vencer imediatamente
        jogada = self.jogada_prioritaria(peca, 5)
        if jogada:
            self.tabuleiro[jogada[0]][jogada[1]] = peca
            return

        # Bloquear vitória do adversário
        jogada = self.jogada_prioritaria(adversario, 5)
        if jogada:
            self.tabuleiro[jogada[0]][jogada[1]] = peca
            return

        # Bloquear 4 em linha do adversário
        jogada = self.jogada_prioritaria(adversario, 4)
        if jogada:
            self.tabuleiro[jogada[0]][jogada[1]] = peca
            return

        # Tentar criar 4 em linha
        jogada = self.jogada_prioritaria(peca, 4)
        if jogada:
            self.tabuleiro[jogada[0]][jogada[1]] = peca
            return

        # Tentar criar 3 em linha
        jogada = self.jogada_prioritaria(peca, 3)
        if jogada:
            self.tabuleiro[jogada[0]][jogada[1]] = peca
            return

        # Encontra uma posição vazia aleatoriamente
        while True:
            linha = randint(0, 9)
            coluna = randint(0, 9)
            if self.tabuleiro[linha][coluna] == ' ':
                self.tabuleiro[linha][coluna] = peca
                break

    def ha_jogadas_possiveis(self) -> bool:
        """
        Verifica se ainda há espaços vazios no tabuleiro.
        :return: True se ainda há jogadas possíveis, False caso contrário.
        """
        return any(celula == ' ' for linha in self.tabuleiro for celula in linha)

    def terminou(self) -> bool:
        """
        Verifica se alguém ganhou (5 peças seguidas em qualquer direção:
        horizontal, vertical, diagonal ↘️, diagonal ↗️).
        :return: True se o jogo terminou (alguém ganhou), False caso contrário.
        """
        direcoes = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for linha in range(10):
            for coluna in range(10):
                celula = self.tabuleiro[linha][coluna]
                if celula != ' ':  # verifica apenas se a célula não estiver vazia
                    for dx, dy in direcoes:
                        # Conta 5 peças na mesma direção
                        contador = 1
                        x, y = linha + dx, coluna + dy
                        while 0 <= x < 10 and 0 <= y < 10 and self.tabuleiro[x][y] == celula:
                            contador += 1
                            x += dx
                            y += dy
                        if contador >= 5:
                            return True
        return False

    def guardar_estado(self, ficheiro: str = 'jogo.pkl') -> None:
        # Guarda o estado do jogo num ficheiro pickle (jogo.pkl default)
        estado = {
            'tabuleiro': self.tabuleiro,
            'jogador_humano': self.jogador_humano
        }
        with open(ficheiro, 'wb') as f:
            pickle.dump(estado, f)
        print(f"Jogo guardado em '{ficheiro}'.")

    def carregar_estado(self, ficheiro: str = 'jogo.pkl') -> None:
        # Carrega o estado do jogo a partir de um ficheiro pickle
        with open(ficheiro, 'rb') as f:
            estado = pickle.load(f)
        self.tabuleiro = estado['tabuleiro']
        self.jogador_humano = estado['jogador_humano']
        print(f"Jogo carregado de '{ficheiro}'.")
