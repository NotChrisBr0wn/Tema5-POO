# gomoku.py (template)
"""
Template para implementar o jogo Gomoku (Cinco em Linha).
Deve implementar todos os métodos abstratos herdados de Jogo.
"""

from jogo_abs import Jogo


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
        raise NotImplementedError("Implementar este método")

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
        raise NotImplementedError("Implementar este método")

    def ha_jogadas_possiveis(self) -> bool:
        """
        Verifica se ainda há espaços vazios no tabuleiro.
        :return: True se ainda há jogadas possíveis, False caso contrário.
        """
        raise NotImplementedError("Implementar este método")

    def terminou(self) -> bool:
        """
        Verifica se alguém ganhou (5 peças seguidas em qualquer direção:
        horizontal, vertical, diagonal ↘️, diagonal ↗️).
        :return: True se o jogo terminou (alguém ganhou), False caso contrário.
        """
        raise NotImplementedError("Implementar este método")
