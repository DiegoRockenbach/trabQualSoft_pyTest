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


def test_SomaEnvidoSemFigura():
    """Verifica se o cálculo dos pontos do envido é feito corretamente"""

    j = Jogador('Test')
    j.mao = [Carta(6, 'ESPADAS'), Carta(2, 'OUROS'), Carta(4, 'ESPADAS')]
    
    result = j.calcula_envido(j.mao)

    assert result == 30

def test_SomaEnvidoComFigura(): #ERROR
    """Verifica se o cálculo dos pontos do envido é feito corretamente"""

    j = Jogador('Test')
    j.mao = [Carta(6, 'ESPADAS'), Carta(2, 'OUROS'), Carta(10, 'ESPADAS')]
    
    #erro na lógica da calcula_envido() 
    result = j.calcula_envido(j.mao)

    assert result == 26

def test_SomaEnvidoComFlorNaMao():
    """Verifica se o cálculo dos pontos do envido é feito corretamente com uma Flor na mão"""

    j = Jogador('Test')
    j.mao = [Carta(6, 'ESPADAS'), Carta(3, 'ESPADAS'), Carta(12, 'ESPADAS')]
    
    result = j.calcula_envido(j.mao)

    assert result == 29

def test_pontuacaoResultadoEnvido(monkeypatch):
    """Verifica se a pontuação é atribuída corretamente ao vencedor do Envido."""

    i = Interface()
    j1 = Jogador('1')
    j1.mao = [Carta(4, 'ESPADAS'), Carta(3, 'ESPADAS'), Carta(6, 'BASTOS')]
    j2 = Jogador('2')
    j2.mao = [Carta(6, 'ESPADAS'), Carta(7, 'ESPADAS'), Carta(12, 'OUROS')]
    
    monkeypatch.setattr(builtins, 'input', lambda *a, **k: '1')

    e = Envido()
    
    j1.envido = j1.calcula_envido(j1.mao) #normalmente é feito em j.criar_mao()
    j2.envido = j2.calcula_envido(j2.mao)

    e.controlador_envido(None, None, 6, 2, j1, j2, i)
    
    assert e.jogador1_pontos == 27
    assert e.jogador2_pontos == 33
    
    assert j1.pontos == 0
    assert j2.pontos == 2
    

def test_pontuacaoResultadoRealEnvido(monkeypatch):
    """Verifica se a pontuação é atribuída corretamente ao vencedor do Real Envido."""

    i = Interface()
    j1 = Jogador('1')
    j1.mao = [Carta(4, 'ESPADAS'), Carta(3, 'ESPADAS'), Carta(6, 'BASTOS')]
    j2 = Jogador('2')
    j2.mao = [Carta(6, 'ESPADAS'), Carta(7, 'ESPADAS'), Carta(12, 'OUROS')]
    
    monkeypatch.setattr(builtins, 'input', lambda *a, **k: '1')

    e = Envido()
    
    j1.envido = j1.calcula_envido(j1.mao) #normalmente é feito em j.criar_mao()
    j2.envido = j2.calcula_envido(j2.mao)

    e.controlador_envido(None, None, 7, 2, j1, j2, i)
    
    assert e.jogador1_pontos == 27
    assert e.jogador2_pontos == 33
    
    assert j1.pontos == 0
    assert j2.pontos == 5

def test_pontuacaoResultadoFaltaEnvidoEmpatado(monkeypatch):
    """Verifica se a pontuação é atribuída corretamente ao vencedor do Falta Envido."""

    i = Interface()
    j1 = Jogador('1')
    j1.mao = [Carta(4, 'ESPADAS'), Carta(3, 'ESPADAS'), Carta(6, 'BASTOS')]
    j2 = Jogador('2')
    j2.mao = [Carta(6, 'ESPADAS'), Carta(7, 'ESPADAS'), Carta(12, 'OUROS')]
    
    monkeypatch.setattr(builtins, 'input', lambda *a, **k: '1')

    e = Envido()
    
    j1.envido = j1.calcula_envido(j1.mao) #normalmente é feito em j.criar_mao()
    j2.envido = j2.calcula_envido(j2.mao)

    e.controlador_envido(None, None, 8, 2, j1, j2, i)
    
    assert e.jogador1_pontos == 27
    assert e.jogador2_pontos == 33
    
    assert j1.pontos == 0
    assert j2.pontos == 12

def test_pontuacaoResultadoFaltaEnvidoDesparelho(monkeypatch):
    """Verifica se a pontuação é atribuída corretamente ao vencedor do Falta Envido."""

    i = Interface()
    j1 = Jogador('1')
    j1.mao = [Carta(4, 'ESPADAS'), Carta(3, 'ESPADAS'), Carta(6, 'BASTOS')]
    j2 = Jogador('2')
    j2.mao = [Carta(6, 'ESPADAS'), Carta(7, 'ESPADAS'), Carta(12, 'OUROS')]
    
    j1.pontos = 8
    j2.pontos = 6

    monkeypatch.setattr(builtins, 'input', lambda *a, **k: '1')

    e = Envido()
    
    j1.envido = j1.calcula_envido(j1.mao) #normalmente é feito em j.criar_mao()
    j2.envido = j2.calcula_envido(j2.mao)

    e.controlador_envido(None, None, 8, 2, j1, j2, i)
    
    assert e.jogador1_pontos == 27
    assert e.jogador2_pontos == 33
    
    assert j1.pontos == 8
    assert j2.pontos == 10 #6+(12-8)