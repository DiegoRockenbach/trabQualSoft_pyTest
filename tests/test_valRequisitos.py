from pathlib import Path
import sys
import pytest
import inspect
import builtins

# Garante que o pacote SOURCE_TRUCO esteja importável durante os testes
ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "SOURCE_TRUCO"
sys.path.insert(0, str(SRC))

from truco.interface import Interface
from truco.truco import Truco
from truco.carta import Carta
from truco.jogador import Jogador
from truco.flor import Flor
from truco.envido import Envido

def test_aumentoValorDeRodadaTruco(monkeypatch): #ERROR
    """Verifica se o valor da rodada aumenta corretamente após um pedido de Truco."""

    monkeypatch.setattr(builtins, 'input', lambda *a, **k: '1')
    
    j1 = Jogador('1')
    j2 = Jogador('2')
    t = Truco()
    t.estado_atual = ""

    # Em uma chamada de truco convencional, truco.valor_aposta não é atualizado. Desse modo, a rodada segue valendo 1 ponto, não importando chamar truco ou não.
    t.controlador_truco(None, None, 2, j1, j2)
    assert t.valor_aposta == 2

def test_aumentoValorDeRodadaRetruco(monkeypatch):
    """Verifica se o valor da rodada aumenta corretamente após um pedido de Retruco."""
    
    monkeypatch.setattr(builtins, 'input', lambda *a, **k: '1')
    
    j1 = Jogador('1')
    j2 = Jogador('2')
    t = Truco()
    t.estado_atual = "truco"

    t.controlador_truco(None, None, 2, j1, j2)
    assert t.valor_aposta == 3

def test_aumentoValorDeRodadaVale4(monkeypatch):
    """Verifica se o valor da rodada aumenta corretamente após um pedido de Vale4."""
    
    monkeypatch.setattr(builtins, 'input', lambda *a, **k: '1')
    
    j1 = Jogador('1')
    j2 = Jogador('2')
    t = Truco()

    t.pedir_vale_quatro(None, 2, j1, j2)
    assert t.valor_aposta == 4

def test_ReconheceFlor(capsys):
    """Verifica se a opção de Flor é reconhecida quando está na mão do jogador."""

    j = Jogador("Test")
    j.mao = [Carta(1, 'ESPADAS'), Carta(2, 'ESPADAS'), Carta(3, 'ESPADAS')]
    j.flor = False

    assert j.checa_flor() == True

def test_PodeChamarFlorAposEnvido(capsys): #ERROR
    """Verifica se a opção de Flor é mostrada após uma chamada de Envido na rodada."""

    j = Jogador("Test")
    e = Envido()
    j.mao = [Carta(1, 'ESPADAS'), Carta(2, 'ESPADAS'), Carta(3, 'ESPADAS')]
    j.flor = False
    j.checa_flor()
    e.estado_atual = '6'
    
    j.mostrar_opcoes(None)
    captured = capsys.readouterr().out #read stdout & stderr, captured é apenas o .out (stdoutput, não stderror)

    assert 'Flor' not in captured



def test_pontuaçãoFlorNormal(monkeypatch):
    """Verifica se a pontuação é atribuída corretamente a quem chamou Flor."""

    i = Interface()
    j1 = Jogador('1')
    j1.mao = [Carta(1, 'BASTOS'), Carta(2, 'OUROS'), Carta(3, 'COPAS')]
    j2 = Jogador('2')
    j2.mao = [Carta(1, 'ESPADAS'), Carta(2, 'ESPADAS'), Carta(3, 'ESPADAS')]
    f = Flor()
    
    j1.flor = j1.checa_flor()
    j2.flor = j2.checa_flor()

    f.pedir_flor(2, j1, j2, i)
    
    assert j1.pontos == 0
    assert j2.pontos == 3

def test_pontuacaoFlorVsFlorFugiu(monkeypatch):
    """Verifica se a chamada de contra flor está funcionando e os pontos estão sendo contabilizados corretamente"""

    i = Interface()
    j1 = Jogador('1')
    j1.mao = [Carta(1, 'ESPADAS'), Carta(2, 'ESPADAS'), Carta(3, 'ESPADAS')]
    j2 = Jogador('2')
    j2.mao = [Carta(1, 'OUROS'), Carta(2, 'OUROS'), Carta(3, 'OUROS')]
    f = Flor()

    j1.flor = j1.checa_flor()
    j2.flor = j2.checa_flor()

    monkeypatch.setattr(builtins, 'input', lambda *a, **k: '0')
    
    f.pedir_flor(2, j1, j2, i)

    assert j1.pontos == 0
    assert j2.pontos == 4

def test_pontuacaoContraFlor(monkeypatch):
    """Verifica se a chamada de contra flor está funcionando e os pontos estão sendo contabilizados corretamente"""

    i = Interface()
    j1 = Jogador('1')
    j1.mao = [Carta(10, 'ESPADAS'), Carta(6, 'ESPADAS'), Carta(7, 'ESPADAS')]
    j2 = Jogador('2')
    j2.mao = [Carta(10, 'OUROS'), Carta(2, 'OUROS'), Carta(3, 'OUROS')]
    
    monkeypatch.setattr(builtins, 'input', lambda *a, **k: '1')


    f = Flor()
    j1.flor = j1.checa_flor()
    j2.flor = j2.checa_flor()
    f.pedir_flor(2, j1, j2, i)

    assert j1.pontos == 6
    assert j2.pontos == 0

def test_pontuacaoContraFlorResto(monkeypatch): #ERROR
    """Verifica se a chamada de contra flor e o resto está funcionando e os pontos estão sendo contabilizados corretamente"""

    i = Interface()
    j1 = Jogador('1')
    j1.mao = [Carta(10, 'ESPADAS'), Carta(6, 'ESPADAS'), Carta(7, 'ESPADAS')]
    j2 = Jogador('2')
    j2.mao = [Carta(10, 'OUROS'), Carta(2, 'OUROS'), Carta(3, 'OUROS')]
    
    monkeypatch.setattr(builtins, 'input', lambda *a, **k: '1')

    e = Envido()
    j1.envido = j1.calcula_envido(j1.mao)
    j2.envido = j2.calcula_envido(j2.mao)
    e.definir_pontos_jogadores(j1, j2)
    assert e.jogador1_pontos == 33
    assert e.jogador2_pontos == 25

    j1.pontos = 5
    j2.pontos = 2 # Por algum motivo a seleção entre Contraflor e Contraflor e Resto depende apenas do check '(jogador2.pontos < int((jogador1.pontos/1.5)))'

    f = Flor()
    j1.flor = j1.checa_flor()
    j2.flor = j2.checa_flor()
    f.pedir_flor(2, j1, j2, i)

    # Contra flor e o resto em nenhum momento atualiza flor.valor_flor (problema similar ao que tem na chamada de truco) então o vencedor ganha apenas 3 pontos (valor da chamada de Flor convencional)
    assert j1.pontos == 12   #j1 fica apenas com 8 pontos (5 anteriores + 3 flor normal, ao invés de 5 + resto)
    assert j2.pontos == 2