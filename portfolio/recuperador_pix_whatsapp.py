"""
Projeto demonstrativo da BLUE ROSE — Recuperação de venda via WhatsApp (PIX)
=============================================================================

Simula, com dados de mentira, o fluxo de automação que a BLUE ROSE monta
pra recuperar vendas perdidas: quando um cliente gera um PIX no checkout e
não paga em X minutos, uma automação (normalmente webhook da plataforma de
pagamento + WhatsApp API) manda uma mensagem lembrando do link de pagamento
— e cancela o envio automaticamente se o pagamento cair antes da hora.

Não usa nenhuma API real de pagamento nem de WhatsApp — os dois pontos de
integração real (`consultar_status_pagamento` e `enviar_mensagem_whatsapp`)
estão isolados em funções próprias, exatamente onde entraria a chamada real
em produção (ex.: webhook da Kirvano/outra plataforma de pagamento + Meta
WhatsApp Cloud API).

Rodar (usa um relógio acelerado, sem esperar minutos de verdade):
    python recuperador_pix_whatsapp.py --pago-em 3
    python recuperador_pix_whatsapp.py --pago-em nunca
"""

import argparse
import time
from dataclasses import dataclass
from datetime import datetime, timedelta


TEMPO_ESPERA_MINUTOS = 10  # configurável — regra pedida pelo cliente


@dataclass
class Pedido:
    id: str
    cliente: str
    valor: float
    status: str = "pix_pendente"  # pix_pendente -> pago | pix_expirado
    gerado_em: datetime = None

    def __post_init__(self):
        if self.gerado_em is None:
            self.gerado_em = datetime.now()


def consultar_status_pagamento(pedido: Pedido) -> str:
    """Ponto único de integração real. Em produção, troca por uma consulta
    ao webhook/API da plataforma de pagamento (ex.: Kirvano)."""
    return pedido.status


def enviar_mensagem_whatsapp(numero: str, texto: str) -> None:
    """Ponto único de integração real. Em produção, troca o print por uma
    chamada HTTP pra WhatsApp Business API/Cloud API."""
    print(f"\n[WhatsApp -> {numero}]\n{texto}\n")


def montar_mensagem_recuperacao(pedido: Pedido) -> str:
    return (
        f"Oi, {pedido.cliente}! Notei que seu pedido #{pedido.id} "
        f"(R$ {pedido.valor:.2f}) ainda está com o PIX pendente. "
        f"Segue o link pra finalizar o pagamento antes que expire: "
        f"[link de pagamento]. Qualquer dúvida, me chama por aqui!"
    )


def processar_pedido(pedido: Pedido, numero_whatsapp: str, minutos_acelerados: float = 1.0) -> None:
    """Simula o fluxo: espera o tempo configurado, consulta o status de
    novo e só manda a mensagem se ainda estiver pendente."""
    print(f"[{datetime.now():%H:%M:%S}] Pedido {pedido.id} criado — PIX gerado, "
          f"aguardando pagamento. Regra: cobrar em {TEMPO_ESPERA_MINUTOS} min se continuar pendente.")

    # No mundo real isso seria um agendamento (cron/fila), não um sleep —
    # aqui aceleramos o tempo só pra demonstração rodar em segundos.
    time.sleep(minutos_acelerados)

    status_atual = consultar_status_pagamento(pedido)
    print(f"[{datetime.now():%H:%M:%S}] Checando status do pedido {pedido.id}: {status_atual}")

    if status_atual == "pago":
        print(f"[{datetime.now():%H:%M:%S}] Pagamento já confirmado — "
              f"automação NÃO envia mensagem (evita incomodar quem já pagou).")
        return

    mensagem = montar_mensagem_recuperacao(pedido)
    enviar_mensagem_whatsapp(numero_whatsapp, mensagem)
    print(f"[{datetime.now():%H:%M:%S}] Mensagem de recuperação enviada pro pedido {pedido.id}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pago-em", default="nunca",
        help="'nunca' (simula cliente que não paga) ou um número de segundos "
             "(simula cliente que paga X segundos depois de gerar o PIX, "
             "antes da automação verificar de novo)."
    )
    args = parser.parse_args()

    pedido = Pedido(id="10234", cliente="Ana", valor=189.90)

    if args.pago_em != "nunca":
        # Simula que o pagamento já caiu quando a automação for checar.
        pedido.status = "pago"

    processar_pedido(pedido, numero_whatsapp="+55 11 9xxxx-xxxx (cliente de exemplo)", minutos_acelerados=1.5)


if __name__ == "__main__":
    main()
