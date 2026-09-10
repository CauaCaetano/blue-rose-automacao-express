"""
Projeto demonstrativo da BLUE ROSE — Qualificador de leads via WhatsApp
========================================================================

Simula, com dados de mentira, o fluxo de automação que a BLUE ROSE monta
com frequência para imobiliárias/corretores: em vez de o corretor perder
tempo respondendo lead por lead manualmente, uma automação (normalmente
n8n + WhatsApp API, aqui simplificado em Python puro para demonstração)
faz uma sequência de perguntas de qualificação e só entrega ao corretor um
resumo pronto do que interessa.

Não usa nenhuma API real de WhatsApp — a função `enviar_mensagem_whatsapp`
é o único ponto onde, em produção, entraria a chamada real (WhatsApp
Business API/Cloud API). Aqui ela só imprime a mensagem no terminal, pra
deixar claro o que seria enviado a cada passo.

Rodar:
    python qualificador_leads_whatsapp.py

Rodar com respostas automáticas de exemplo (sem digitar nada):
    python qualificador_leads_whatsapp.py --demo
"""

import argparse
import sys
from dataclasses import dataclass, field
from datetime import datetime

# Garante saída em UTF-8 mesmo no cmd/PowerShell com codepage padrão
# (evita acento virar caractere estranho no terminal do Windows).
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass


def enviar_mensagem_whatsapp(numero: str, texto: str) -> None:
    """Ponto único de integração real. Em produção, troca o print por uma
    chamada HTTP pra WhatsApp Business API/Cloud API."""
    print(f"\n[WhatsApp -> {numero}]\n{texto}\n")


@dataclass
class Lead:
    numero: str
    tipo_imovel: str = ""
    regiao: str = ""
    orcamento: str = ""
    prazo: str = ""
    respostas_livres: list = field(default_factory=list)


PERGUNTAS = [
    ("tipo_imovel", "Oi! Vi seu interesse no anúncio :) Pra eu te ajudar melhor: "
                     "você procura apartamento, casa ou terreno?"),
    ("regiao", "Show! E em qual região/bairro você tem preferência (ou está aberto a sugestões)?"),
    ("orcamento", "Perfeito. Qual faixa de orçamento você tem em mente pro imóvel?"),
    ("prazo", "Última pergunta: você pretende fechar negócio em quanto tempo "
              "(esse mês, nos próximos 3 meses, ou só pesquisando por enquanto)?"),
]


def qualificar(numero: str, respostas_demo: list[str] | None = None) -> Lead:
    lead = Lead(numero=numero)
    campos = [p[0] for p in PERGUNTAS]

    for i, (campo, pergunta) in enumerate(PERGUNTAS):
        enviar_mensagem_whatsapp(numero, pergunta)
        if respostas_demo is not None:
            resposta = respostas_demo[i]
            print(f"[Lead responde] {resposta}")
        else:
            resposta = input("[Lead responde] ")
        setattr(lead, campo, resposta)

    return lead


def classificar_qualidade(lead: Lead) -> str:
    """Regra simples de exemplo — em produção isso pode usar um modelo de
    IA pra interpretar respostas livres em vez de perguntas fechadas."""
    sinais_bons = 0
    if lead.prazo.lower() not in ("", "só pesquisando", "so pesquisando"):
        sinais_bons += 1
    if lead.orcamento.strip() != "":
        sinais_bons += 1
    if lead.regiao.strip() != "":
        sinais_bons += 1

    if sinais_bons >= 3:
        return "QUENTE"
    if sinais_bons == 2:
        return "MORNO"
    return "FRIO"


def resumo_para_corretor(lead: Lead) -> str:
    qualidade = classificar_qualidade(lead)
    return (
        f"--- Novo lead qualificado ({datetime.now():%d/%m %H:%M}) ---\n"
        f"WhatsApp: {lead.numero}\n"
        f"Classificação: {qualidade}\n"
        f"Tipo de imóvel: {lead.tipo_imovel}\n"
        f"Região: {lead.regiao}\n"
        f"Orçamento: {lead.orcamento}\n"
        f"Prazo: {lead.prazo}\n"
        f"---------------------------------------------"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true",
                         help="usa respostas de exemplo em vez de pedir input")
    args = parser.parse_args()

    numero_exemplo = "+55 11 9xxxx-xxxx (lead de exemplo)"

    if args.demo:
        respostas_demo = ["apartamento", "Zona Sul", "até R$ 350 mil", "nos próximos 3 meses"]
        lead = qualificar(numero_exemplo, respostas_demo)
    else:
        print("Respondendo como o LEAD (digite as respostas). Ctrl+C pra sair.\n")
        lead = qualificar(numero_exemplo)

    print("\n" + resumo_para_corretor(lead))
    print("\n>>> Esse resumo é o que chegaria pronto pro corretor, em vez de "
          "ele ter que ler a conversa inteira do zero.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
