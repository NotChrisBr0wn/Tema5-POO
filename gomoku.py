# gomoku.py (template)
"""
Template para implementar o jogo Gomoku (Cinco em Linha).
Deve implementar todos os métodos abstratos herdados de Jogo.
"""

import pickle
from jogo_abs import Jogo
from random import randint
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=False)


class Gomoku(Jogo):
    """
    Classe concreta que herda da classe Jogo e implementa o jogo Gomoku.
    """
    def __init__(self) -> None:
        super().__init__()
        self.jogador_humano = None
        self.modo_hotseat: bool = False
        self.nomes_hotseat: dict[int, str] | None = None
        self.score_hotseat: dict[int, int] | None = None
        self.jogador_atual_hotseat: int | None = None
        self._acabou_de_carregar_hotseat: bool = False
        self.historico: list[list[list[str]]] = []
        self.redo: list[list[list[str]]] = []

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
        reset = Style.RESET_ALL
        fundo = Back.BLACK

        print()
        cabecalho = fundo + "  | " + " | ".join(str(c) for c in range(10)) + " |" + reset
        print(cabecalho)

        for i, linha in enumerate(self.tabuleiro):
            linha_str = f"{fundo}{i} |"
            for celula in linha:
                if celula == 'X':
                    linha_str += f" {Back.BLACK}{Fore.RED}{Style.BRIGHT}X{reset}{fundo} |"
                elif celula == 'O':
                    linha_str += f" {Back.BLACK}{Fore.BLUE}{Style.BRIGHT}O{reset}{fundo} |"
                else:
                    linha_str += "   |"
            print(linha_str + reset)
        print()

    def _snapshot_tabuleiro(self) -> list[list[str]]:
        # Cria uma cópia do tabuleiro atual
        return [linha[:] for linha in self.tabuleiro]

    def guardar_jogada(self) -> None:
        # Guarda o estado atual para poder desfazer e limpa o histórico de refazer
        self.historico.append(self._snapshot_tabuleiro())
        self.redo.clear()

    def desfazer(self) -> bool:
        # Desfaz a última jogada
        if not self.historico:
            print("Nada para desfazer.")
            return False

        self.redo.append(self._snapshot_tabuleiro())
        self.tabuleiro = self.historico.pop()
        print("Última jogada desfeita.")
        return True

    def refazer(self) -> bool:
        # Refaz a última jogada desfeita
        if not self.redo:
            print("Nada para refazer.")
            return False

        self.historico.append(self._snapshot_tabuleiro())
        self.tabuleiro = self.redo.pop()
        print("Jogada refeita.")
        return True

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
                coords = input(
                    f"Jogador {jogador} ({peca}), introduza linha coluna (0-9), "
                    "'s' guardar, 'c' carregar, 'u' desfazer, 'r' refazer, 'q' sair: "
                )

                if coords.strip().lower() == 's':
                    self.guardar_estado()
                    continue
                if coords.strip().lower() == 'c':
                    self.carregar_estado()
                    self.mostra_tabuleiro()
                    if self.modo_hotseat:
                        return
                    continue
                if coords.strip().lower() == 'u':
                    self.desfazer()
                    self.mostra_tabuleiro()
                    continue
                if coords.strip().lower() == 'r':
                    self.refazer()
                    self.mostra_tabuleiro()
                    continue
                if coords.strip().lower() == 'q':
                    print("A sair do jogo...")
                    exit()

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
                self.guardar_jogada()
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
            self.guardar_jogada()
            self.tabuleiro[jogada[0]][jogada[1]] = peca
            return

        # Bloquear vitória do adversário
        jogada = self.jogada_prioritaria(adversario, 5)
        if jogada:
            self.guardar_jogada()
            self.tabuleiro[jogada[0]][jogada[1]] = peca
            return

        # Bloquear 4 em linha do adversário
        jogada = self.jogada_prioritaria(adversario, 4)
        if jogada:
            self.guardar_jogada()
            self.tabuleiro[jogada[0]][jogada[1]] = peca
            return

        # Tentar criar 4 em linha
        jogada = self.jogada_prioritaria(peca, 4)
        if jogada:
            self.guardar_jogada()
            self.tabuleiro[jogada[0]][jogada[1]] = peca
            return

        # Tentar criar 3 em linha
        jogada = self.jogada_prioritaria(peca, 3)
        if jogada:
            self.guardar_jogada()
            self.tabuleiro[jogada[0]][jogada[1]] = peca
            return

        # Encontra uma posição vazia aleatoriamente
        while True:
            linha = randint(0, 9)
            coluna = randint(0, 9)
            if self.tabuleiro[linha][coluna] == ' ':
                self.guardar_jogada()
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
            'jogador_humano': self.jogador_humano,
            'modo_hotseat': self.modo_hotseat,
            'nomes_hotseat': self.nomes_hotseat,
            'score_hotseat': self.score_hotseat,
            'jogador_atual_hotseat': self.jogador_atual_hotseat,
            'historico': self.historico,
            'redo': self.redo,
        }
        with open(ficheiro, 'wb') as f:
            pickle.dump(estado, f)
        print(f"Jogo guardado em '{ficheiro}'.")

    def carregar_estado(self, ficheiro: str = 'jogo.pkl') -> None:
        # Carrega o estado do jogo a partir de um ficheiro pickle
        try:
            with open(ficheiro, 'rb') as f:
                estado = pickle.load(f)
        except FileNotFoundError:
            print(f"Ficheiro '{ficheiro}' não encontrado.")
            return

        self.tabuleiro = estado['tabuleiro']
        self.jogador_humano = estado.get('jogador_humano')

        # Carrega estado do modo 2 jogadores
        if estado.get('modo_hotseat'):
            self.modo_hotseat = True
            self.nomes_hotseat = estado.get('nomes_hotseat')
            self.score_hotseat = estado.get('score_hotseat')
            self.jogador_atual_hotseat = estado.get('jogador_atual_hotseat')
            self._acabou_de_carregar_hotseat = True

        self.historico = estado.get('historico', [])
        self.redo = estado.get('redo', [])

        print(f"Jogo carregado de '{ficheiro}'.")

    def hotseat(self) -> None:
        # Modo dois jogadores com pontuação acumulada
        nome0 = input("Nome do Jogador 0 (O): ").strip() or "Jogador 0"
        nome1 = input("Nome do Jogador 1 (X): ").strip() or "Jogador 1"
        nomes = {0: nome0, 1: nome1}
        score = {0: 0, 1: 0}

        self.modo_hotseat = True
        self.nomes_hotseat = nomes
        self.score_hotseat = score

        while True:
            self.inicializa_tabuleiro()
            jogador = 0

            while True:
                self.mostra_tabuleiro()
                print(f"Vez de {nomes[jogador]}")

                # Guarda a vez atual
                self.jogador_atual_hotseat = jogador
                self.joga_humano(jogador)

                # Se carregar estado repoe o jogador atual e pontuação
                if self._acabou_de_carregar_hotseat:
                    if self.nomes_hotseat is not None:
                        nomes = self.nomes_hotseat
                    if self.score_hotseat is not None:
                        score = self.score_hotseat
                    if self.jogador_atual_hotseat is not None:
                        jogador = self.jogador_atual_hotseat
                    self._acabou_de_carregar_hotseat = False
                    continue

                if self.terminou():
                    self.mostra_tabuleiro()
                    score[jogador] += 1
                    print(f"\n{nomes[jogador]} ganhou!")
                    print(f"Pontuação: {nomes[0]} = {score[0]} | {nomes[1]} = {score[1]}")
                    break

                if not self.ha_jogadas_possiveis():
                    self.mostra_tabuleiro()
                    print("\nEmpate!")
                    print(f"Pontuação: {nomes[0]} = {score[0]} | {nomes[1]} = {score[1]}")
                    break

                jogador = (jogador + 1) % 2

            again = input("\nJogar novamente? (s/n): ").strip().lower()
            if again != 's':
                print(f"\nPontuação final: {nomes[0]} = {score[0]} | {nomes[1]} = {score[1]}")
                print("Obrigado por jogar!")
                break

def _mostra_menu() -> None:
    titulo = Back.YELLOW + Fore.BLACK + Style.BRIGHT
    reset = Style.RESET_ALL
    print()
    print(titulo + "  ╔══════════════════════╗  " + reset)
    print(titulo + "  ║        GOMOKU        ║  " + reset)  
    print(titulo + "  ╚══════════════════════╝  " + reset)
    print()
    print("  1. Novo jogo (vs Computador)")
    print("  2. 2 Jogadores")
    print("  0. Sair")
    print()


def menu() -> None:
    _mostra_menu()

    while True:
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            jogo = Gomoku()
            jogo.jogar()
        elif opcao == '2':
            jogo = Gomoku()
            jogo.hotseat()
        elif opcao == '0':
            print("Até logo!")
            break
        else:
            print("Opção inválida. Escolha 0, 1 ou 2.")
            continue

        _mostra_menu()


if __name__ == "__main__":
    menu()
