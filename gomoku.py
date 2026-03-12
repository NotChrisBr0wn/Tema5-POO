# gomoku.py (template)
"""
Template para implementar o jogo Gomoku (Cinco em Linha).
Deve implementar todos os métodos abstratos herdados de Jogo.
"""

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
        print("  " + " ".join(str(c) for c in range(10)))
        for i, linha in enumerate(self.tabuleiro):
            print(f"{i} " + "|".join(linha))

    def joga_humano(self, jogador: int) -> None:
        """
        Pede ao jogador humano as coordenadas (linha, coluna) da jogada
        e coloca a peça no tabuleiro.
        - Jogador 0 usa 'O', Jogador 1 usa 'X'.
        - Deve validar se a posição está dentro do tabuleiro e está livre.
        :param jogador: número do jogador (0 ou 1).
        """
        raise NotImplementedError("Implementar este método")

    def joga_computador(self, jogador: int) -> None:
        """
        Realiza uma jogada aleatória do computador numa posição livre.
        - Jogador 0 usa 'O', Jogador 1 usa 'X'.
        :param jogador: número do jogador (computador).
        """
        peca = 'O' if jogador == 0 else 'X'
        
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
