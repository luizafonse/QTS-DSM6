import pytest 
from app.main import calcular_faturamento

@pytest.mark.unit
def test_faturamento_plano_basico_sem_cupom():
    resultado = calcular_faturamento("basico")
    assert resultado == 50.0
    
@pytest.mark.unit
def test_faturamento_plano_procom_cupom_porcentagem():
    resultado = calcular_faturamento("pro")
    assert resultado == 135.0
    
@pytest.mark.unit
def test_faturamento_com_atraso():
    resultado = calcular_faturamento("basico", dias_atraso=10)
    assert resultado == 60.0