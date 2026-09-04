import pytest
from app.schemas import SolicitacaoCredito
from app.service import avaliar_solicitacao_credito
 
# particionamento de equivalencia e valor limite: idade
 
@pytest.mark.unit
@pytest.mark.blackbox
@pytest.mark.parametrize(
    "idade_invalida, mensagem_esperada",
    [
        (17, "Idade minima permitida e 18 anos."),
        (0, "Idade minima permitida e 18 anos."),
        (-5, "Idade minima permitida e 18 anos."),
        (76, "Idade maxima permitida e 75 anos."),
        (100, "Idade maxima permitida e 75 anos."),
    ],
    ids = ["bva_17_abaixo_limite", "zero_idade", "negativo_idade", "bva_76_acima_limite", "cem_anos"]
)
def test_bva_idade_deve_lancar_erro(idade_invalida: int, mensagem_esperada: str):
    """ Testa a validacao de idade com particionamento de equivalencia e valor limite. """
    solicitacao = SolicitacaoCredito(
        idade=idade_invalida,
        renda_mensal=5000.0,
        score_serasa=700,
        valor_solicitado=5000.0,
        quantidade_parcelas=12
    )
    with pytest.raises(ValueError, match=mensagem_esperada):
        avaliar_solicitacao_credito(solicitacao)
 
@pytest.mark.unit
@pytest.mark.blackbox
@pytest.mark.parametrize(
    "idade_valida",
    [
        (18),
        (19),
        (45),
        (74),
        (75)
    ],
    ids = ["bva_18_minimo_exato", "bva_19_um_acima_minimo", "particao_valida_media", "bva_74_um_abaixo_maximo", "bva_75_maximo_exato"]
)
def test_bva_idade_valida_deve_processar_com_sucesso(idade_valida: int):
    """Valida valores limites validos para o campo idade"""
    solicitacao = SolicitacaoCredito(
        idade=idade_valida,
        renda_mensal=5000.0,
        score_serasa=700,
        valor_solicitado=5000.0,
        quantidade_parcelas=12
    )
    resultado = avaliar_solicitacao_credito(solicitacao)
    assert resultado.status == "APROVADO"
    
# 2 Particionamento de Equivalência e valor limite: SCORE SERASA
@pytest.mark.unit
@pytest.mark.blackbox
@pytest.mark.parametrize(
    "score_invalido",
    [-1, -100, 1001, 1500],
    ids=["bva_menos_um", "negativo_extremo", "bva_1001", "acima_extremo"]
)
 
def test_bva_score_invalido_deve_lancar_erro(score_invalido: int) :
    """ Valida limites externos invalidos para score de credito. """
    solicitacao = SolicitacaoCredito(
                idade=30,
                renda_mensal=5000.0,
                score_serasa=score_invalido,
                valor_solicitado=5000.0,
                quantidade_parcelas=12
        )
    with pytest.raises(ValueError, match="Score Serasa deve estar entre 0 e 1000"):
        avaliar_solicitacao_credito(solicitacao)
 
@pytest.mark.unit
@pytest.mark.blackbox
def test_regra_restricao_cadastral_reprova_automaticamente():
    """ Valida se o solicitante com restrição ativa é reprovado mesmo com score e renda altos. """    
    solicitacao = SolicitacaoCredito(
                idade=35,
                renda_mensal=5000.0,
                score_serasa=950,
                valor_solicitado=5000.0,
                quantidade_parcelas=12,
                possui_restricao_nome=True
    )
    resultado = avaliar_solicitacao_credito(solicitacao)
    assert resultado.status == "REPROVADO"
    assert resultado.categoria_risco == "RESTRICAO"
    assert resultado.limite_maximo_aprovado == 0.0
    assert "Restricao cadastral" in resultado.motivo