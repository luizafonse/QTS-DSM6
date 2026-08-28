import pytest
from app.main import calcular_faturamento

@pytest.mark.unit 
def test_eror_guessing_cupom_com_espacos_em_branco():
    with pytest.raises(ValueError) as excinfo:
        resultado = calcular_faturamento("basico", cupom="  ")
    assert resultado == 50.0
    
@pytest.mark.unit
def test_eror_guessing_dias_atraso_negativo_deve_lancar_erro():
    with pytest.raises(ValueError, match="Dias de atraso não podem ser negativos"):
        resultado = calcular_faturamento("pro", dias_atraso=-3)
        
@pytest.mark.unit
def test_error_guessing_desconto_nao_pode_gerar_fatura_negativa():
    resultado = calcular_faturamento("basico", cupom="BEMVINDO50")
    assert resultado >= 0.0
    
@pytest.mark.unit
def test_error_guessing_plano_com_espacos_extras():
    resultado = calcular_faturamento("  pro  ")
    assert resultado == 150.0