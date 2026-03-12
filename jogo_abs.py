# jogo_abs.py
"""
Interface de um jogo para 2 jogadores.
"""

from abc import ABC, abstractmethod
from random import randint
from typing import Optional


class Jogo(ABC):
    """
    Classe abstrata que define a interface de um jogo para 2 jogadores.
    """

    def __init__(self) -> None:
        """
        Inicializar o jogo.
        """
        print("Bom jogo...")

        self.num_jogador_humano = None
        self.inicializa_tabuleiro()

    @abstractmethod
    def inicializa_tabuleiro(self) -> None:
        """
        Inicializar o tabuleiro do jogo.
        """
        raise NotImplementedError("A subclasse tem de implementar este método.")

    @abstractmethod
    def mostra_tabuleiro(self) -> None:
        """
        Desenhar o tabuleiro do jogo.
        """
        raise NotImplementedError("A subclasse tem de implementar este método.")

    @abstractmethod
    def joga_humano(self, jogador: int) -> None:
        """
        Solicitar ao humano :jogador: a próxima jogada
        e colocá-la no tabuleiro.
        :param jogador: número do jogador (0 ou 1).
        """
        raise NotImplementedError("A subclasse tem de implementar este método.")

    @abstractmethod
    def joga_computador(self, jogador: int) -> None:
        """
        Realizar a jogada do computador.
        :param jogador: número do jogador (computador).
        """
        raise NotImplementedError("A subclasse tem de implementar este método.")

    @abstractmethod
    def ha_jogadas_possiveis(self) -> bool:
        """
        Verifica se ainda há jogadas possíveis ou se o jogo está empatado.
        :return: `True` se ainda há jogadas possíveis, `False` caso contrário.
        """
        raise NotImplementedError("A subclasse tem de implementar este método.")

    @abstractmethod
    def terminou(self) -> bool:
        """
        Verifica se foi verificada a condição de paragem, i.e., um jogador ganhou.
        :return: `True` se o jogo terminou, `False` caso contrário.
        """
        raise NotImplementedError("A subclasse tem de implementar este método.")

    @property
    def jogador_humano(self) -> Optional[int]:
        """
        Obtém o número do jogador humano.
        :return: número do jogador humano (0 ou 1, ou None se não definido)
        """
        return self.__num_jogador_humano

    @jogador_humano.setter
    def jogador_humano(self, valor: Optional[int]) -> None:
        """
        Define o número do jogador humano.
        :param valor: número do jogador (deve ser 0 ou 1, ou None durante a inicialização)
        :raises ValueError: se o valor não for 0 ou 1 (None é permitido apenas durante a inicialização)
        """
        if valor is not None and valor not in (0, 1):
            raise ValueError("O jogador humano deve ser 0 ou 1")
        self.__num_jogador_humano = valor

    def jogar(self, jogador_humano: Optional[int] = None) -> int:
        """
        Corre o jogo.
        :param jogador_humano: (opcional) número do jogador humano para testes
        :return: número do jogador vencedor, ou -1 em caso de empate
        """

        jogador = 0

        # Escolher número do jogador humano
        if jogador_humano is not None:
            self.jogador_humano = jogador_humano
        else:
            self.jogador_humano = randint(0, 1)

        while True:
            self.mostra_tabuleiro()

            if jogador == self.jogador_humano:
                self.joga_humano(jogador)
            else:
                self.joga_computador(jogador)

            # Verificar se o jogo terminou (alguém ganhou)
            if self.terminou():
                self.mostra_tabuleiro()
                print(f"\nO jogador {jogador} ganhou!")
                return jogador

            # Verificar se houve empate
            if not self.ha_jogadas_possiveis():
                self.mostra_tabuleiro()
                print("\nEmpataram...")
                return -1

            # Passar a vez ao outro jogador
            jogador = (jogador + 1) % 2  # 0->1 ou 1->0


"""
Este ficheiro utiliza "type annotations" em Python.
Type annotations são uma forma de indicar o tipo esperado de uma variável,
parâmetro de função ou valor de retorno de função.
Embora type annotations não sejam obrigatórias em Python, melhoram a
legibilidade do código e permitem que ferramentas de análise estática
(como linters e type checkers) verifiquem a correção do código.

Exemplos:
    def soma(x: int, y: int) -> int:
        return x + y

Neste exemplo, `x: int` e `y: int` indicam que os parâmetros `x` e `y`
devem ser do tipo inteiro, e `-> int` indica que a função `soma`
deve retornar um valor do tipo inteiro.

    from typing import Optional

    def encontra_elemento(lista: list, elemento: any) -> Optional[int]:
        if elemento in lista:
            return lista.index(elemento)
        else:
            return None

No exemplo acima, `Optional[int]` indica que a função `encontra_elemento`
pode retornar um valor do tipo inteiro (`int`) ou `None`. Isto é útil
para explicitar que a função pode não retornar um inteiro em todos os casos,
por exemplo, quando o elemento não é encontrado na lista. `Optional[T]`
é equivalente a `Union[T, None]`.
"""
