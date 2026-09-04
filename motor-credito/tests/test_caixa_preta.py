import pytest
from app.schemas import SolicitacaoCredito
from app.service import avaliar_solicitacao_credito

#particionamento de equivalencia e valor limite : idade

@pytest.mark.unit
@pytest.mark.blackbox
@pytest.mark.parametrize(
    "idade_invalida, mensagem_esperada ",
    [
        (17, "Idade mínima para solicitação de crédito é 18 anos."),# idade abaixo do limite
        (0, "Idade mínima para solicitação de crédito é 18 anos."),
        (-5, "Idade mínima para solicitação de crédito é 18 anos."),  # idade no limite inferior
        (76, "Idade máxima para solicitação de crédito é 75 anos."),  # idade no limite superior
        (100, "Idade máxima para solicitação de crédito é 75 anos."),  # idade acima do limite
    ],
    ids=["bva_17_abaixo_limite", "zero_idade", "negativo_idade", "bva_76_acima_limite", "cem_anos"]
)
def test_bva_idade_invalida_deve_lancar_erro(idade_invalida: int, mensagem_esperada: str):
    solicitacao = SolicitacaoCredito(
        idade=idade_invalida,
        renda_mensal=5000.0,
        score_serasa=700,
        valor_solicitado=5000.0,
        quantidade_parcelas=12
    )
    with pytest.raises(ValueError, match=mensagem_esperada):
        avaliar_solicitacao_credito(solicitacao)