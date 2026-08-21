import pytest

from app.main import calcular_frete
# teste unitario

# nao é obrigatorio, é apenas uma boa prática, para sabermos a categoria e porcentagem de cobertura

@pytest.mark.unit

# o nome do test deve sempre esar ingles, ter underline e deve descrever exatamente o que faz

def test_frete_peso_invalido_zero_ou_negativo():

  with pytest.raises(ValueError, match="O peso deve ser maior que zero"):

    calcular_frete(peso= 0.0, uf="SP")

  

  with pytest.raises(ValueError, match="O peso deve ser maior que zero"):

    calcular_frete(peso=-5.0, uf="SP")

  

@pytest.mark.unit

def test_frete_excede_limite_maximo():

  assert calcular_frete(peso = 30.0, uf="SP") == 50.0

# TESTE DE BORDA, TESTANDO O PRIMEIRO DECIMO ACIMA DO LIMITE PARA EVITAR PROBLEMAS DE SISTEMAS Q

# ARREDONDEM O VALOR

  with pytest.raises(ValueError, match="O peso excede o limite máximo permitido de 30kg"):

    calcular_frete(peso= 30.1, uf="SP")

  

@pytest.mark.unit

def test_frete_uf_invalida():

  with pytest.raises(ValueError, match="UF invalida"):

    calcular_frete(peso=5.0, uf="XX")

  

@pytest.mark.unit

def teste_frete_normalizacao_uf():

  assert calcular_frete(peso=5.0, uf="sp") == 20.0

  assert calcular_frete(peso=5.0, uf="am") == 35.0

  

# passando diversos testes de uma vez com uma função so

@pytest.mark.parametrize("peso, uf, esperado", [

  (0.01, "SP", 20.0),

  (10.0, "SP", 20.0),

  (10.01, "SP", 50.0),

  (30.0, "SP", 50.0),

  (5.0, "AM", 35.0),

  (15.0, "AM", 65.0),

  (5.0, "RJ", 20.0),

])

@pytest.mark.unit

def test_frete_calculos_validos_parametrizados(peso, uf, esperado):

  assert calcular_frete(peso=peso, uf=uf) == esperado