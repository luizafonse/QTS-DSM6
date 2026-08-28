# app/main.py
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Motor de Faturamento de Assinaturas")

VALORES_PLANOS = {
    "BASICO": 50.0,
    "PRO": 150.0,
    "ENTERPRISE": 500.0
}

CUPONS_VALIDOS = {
    "PROMO10": ("PORCENTAGEM", 10.0),
    "DESCONTO20": ("PORCENTAGEM", 20.0),
    "BEMVINDO50": ("FIXO", 50.0)
}

class RequisicaoFatura(BaseModel):
    plano: str
    cupom: Optional[str] = None
    dias_atraso: int = 0

def calcular_faturamento(plano: str, cupom: Optional[str] = None, dias_atraso: int = 0) -> float:
    plano_upper = plano.upper()
    if plano_upper not in VALORES_PLANOS:
        raise ValueError(f"Plano invalido: {plano}")

    valor_base = VALORES_PLANOS[plano_upper]
    valor_com_desconto = valor_base

    if cupom:
        cupom_upper = cupom.upper()
        if cupom_upper in CUPONS_VALIDOS:
            tipo, taxa = CUPONS_VALIDOS[cupom_upper]
            if tipo == "PORCENTAGEM":
                valor_com_desconto = valor_base - (valor_base * (taxa / 100))
            elif tipo == "FIXO":
                valor_com_desconto = valor_base - taxa
        else:
            raise ValueError(f"Cupom invalido: {cupom}")

    if dias_atraso > 0:
        multa = 5.0
        juros = valor_com_desconto * (0.01 * dias_atraso)
        valor_final = valor_com_desconto + multa + juros
    else:
        valor_final = valor_com_desconto

    return round(valor_final, 2)