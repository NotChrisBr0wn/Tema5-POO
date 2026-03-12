# test_gomoku.py
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pytest",
# ]
# ///
import pytest
from gomoku import Gomoku

@pytest.fixture
def jogo():
    """
    Configuração inicial para cada teste.
    """
    return Gomoku()

def test_inicializacao(jogo):
    """Verifica se o tabuleiro é inicializado corretamente (10x10 vazio)."""
    assert len(jogo.tabuleiro) == 10
    assert len(jogo.tabuleiro[0]) == 10
    for linha in jogo.tabuleiro:
        for celula in linha:
            assert celula == ' '

def test_ha_jogadas_possiveis_inicio(jogo):
    """No início, deve haver jogadas possíveis."""
    assert jogo.ha_jogadas_possiveis() is True

def test_ha_jogadas_possiveis_cheio(jogo):
    """Se o tabuleiro estiver cheio, não deve haver jogadas possíveis."""
    jogo.tabuleiro = [['X' for _ in range(10)] for _ in range(10)]
    assert jogo.ha_jogadas_possiveis() is False

def test_mostra_tabuleiro(capsys, jogo):
    """Verifica se o tabuleiro é mostrado corretamente."""
    jogo.tabuleiro[0][0] = 'X'
    jogo.tabuleiro[5][5] = 'O'

    jogo.mostra_tabuleiro()

    captured = capsys.readouterr()
    output = captured.out
    assert 'X' in output
    assert 'O' in output
    # Verifica que os números de coluna estão presentes
    assert '0' in output
    assert '9' in output

def test_joga_humano_posicao_valida(monkeypatch, jogo):
    """Verifica se o método joga_humano coloca a peça corretamente."""
    monkeypatch.setattr('builtins.input', lambda _: '3 4')
    jogo.joga_humano(0)  # Jogador 0 usa 'O'
    assert jogo.tabuleiro[3][4] == 'O'

def test_joga_humano_posicao_ocupada(monkeypatch, jogo):
    """Verifica se o método joga_humano rejeita posição ocupada e pede outra."""
    inputs = iter(['3 4', '5 5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    jogo.tabuleiro[3][4] = 'X'  # Ocupa a posição

    jogo.joga_humano(1)  # Jogador 1 usa 'X'

    # A primeira tentativa (3,4) deve falhar, a segunda (5,5) deve funcionar
    assert jogo.tabuleiro[5][5] == 'X'

def test_joga_computador_valida(jogo):
    """Verifica se o computador joga numa casa válida."""
    # Enche o tabuleiro exceto uma casa
    jogo.tabuleiro = [['X' for _ in range(10)] for _ in range(10)]
    jogo.tabuleiro[5][5] = ' '

    jogo.joga_computador(0)  # Jogador 0 usa 'O'

    assert jogo.tabuleiro[5][5] == 'O'

def test_vitoria_horizontal(jogo):
    """Testa vitória com 5 peças na horizontal."""
    for i in range(5):
        jogo.tabuleiro[0][i] = 'X'
    assert jogo.terminou() is True

def test_vitoria_vertical(jogo):
    """Testa vitória com 5 peças na vertical."""
    for i in range(5):
        jogo.tabuleiro[i][0] = 'O'
    assert jogo.terminou() is True

def test_vitoria_diagonal_desc(jogo):
    """Testa vitória na diagonal descendente (↘️)."""
    for i in range(5):
        jogo.tabuleiro[i][i] = 'X'
    assert jogo.terminou() is True

def test_vitoria_diagonal_asc(jogo):
    """Testa vitória na diagonal ascendente (↗️)."""
    for i in range(5):
        jogo.tabuleiro[4-i][i] = 'O'
    assert jogo.terminou() is True

def test_nao_terminou_4_pecas(jogo):
    """4 peças em linha não devem contar como vitória."""
    for i in range(4):
        jogo.tabuleiro[0][i] = 'X'
    assert jogo.terminou() is False

def test_nao_terminou_pecas_dispersas(jogo):
    """Peças dispersas não devem contar como vitória."""
    jogo.tabuleiro[0][0] = 'X'
    jogo.tabuleiro[0][2] = 'X'
    jogo.tabuleiro[0][4] = 'X'
    jogo.tabuleiro[0][6] = 'X'
    jogo.tabuleiro[0][8] = 'X'
    assert jogo.terminou() is False

def test_jogar_partida_vitoria(monkeypatch, jogo):
    """Verifica se o método jogar funciona para uma partida com vitória."""
    rand_vals = iter([0, 4])
    monkeypatch.setattr('gomoku.randint', lambda a, b: next(rand_vals))
    
    # Configura o tabuleiro para que o jogador 0 vença na próxima jogada
    for i in range(4):
        jogo.tabuleiro[0][i] = 'O'

    # Força jogador_humano a ser 1 (computador é jogador 0)
    resultado = jogo.jogar(jogador_humano=1)

    # Verifica se o jogo foi vencido pelo jogador 0
    assert resultado == 0

def test_jogar_empate(monkeypatch, jogo):
    """Verifica se o método jogar retorna -1 em caso de empate."""
    # Preenche o tabuleiro sem nenhuma vitória, deixando uma casa livre.
    # Padrão: alterna a cada 2 colunas para impedir 5 em linha.
    # Linhas pares: O O X X O O X X O O
    # Linhas ímpares: X X O O X X O O X X
    for l in range(10):
        for c in range(10):
            bloco = (c // 2) % 2  # 0,0,1,1,0,0,1,1,0,0
            if l % 2 == 0:
                jogo.tabuleiro[l][c] = 'O' if bloco == 0 else 'X'
            else:
                jogo.tabuleiro[l][c] = 'X' if bloco == 0 else 'O'

    # Deixa uma casa livre para o computador jogar
    jogo.tabuleiro[9][9] = ' '

    # Força jogador_humano a ser 1 (computador é jogador 0)
    monkeypatch.setattr('gomoku.randint', lambda a, b: 9)
    resultado = jogo.jogar(jogador_humano=1)

    assert resultado == -1


if __name__ == '__main__':
    import sys
    sys.exit(pytest.main(["-v", __file__]))
