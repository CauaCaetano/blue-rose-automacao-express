"""
Utilitário — abrir o navegador (Chrome já instalado) e navegar para uma URL.

Usa Playwright com channel="chrome" (usa o Chrome já instalado no sistema em
vez de baixar um Chromium separado). Roda headless por padrão (não abre
janela visível) — use --visivel para ver a janela abrir de verdade.

Regra de segurança: este utilitário só navega e lê a página. Nunca preenche
formulário, clica em botão de pagamento/login ou envia dado nenhum — isso é
feito só por scripts específicos, revisados caso a caso.

Uso:
    python navegador.py https://example.com [--visivel]
"""

import argparse
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

PASTA_SCREENSHOTS = Path(__file__).resolve().parent.parent / "logs" / "screenshots"


def navegar(url: str, visivel: bool = False):
    PASTA_SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        navegador = p.chromium.launch(channel="chrome", headless=not visivel)
        pagina = navegador.new_page()
        pagina.goto(url, wait_until="load", timeout=15000)

        titulo = pagina.title()
        texto = pagina.inner_text("body")[:300]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_print = PASTA_SCREENSHOTS / f"navegador_{timestamp}.png"
        pagina.screenshot(path=str(caminho_print))

        navegador.close()

    return {
        "url": url,
        "titulo": titulo,
        "trecho_texto": texto,
        "screenshot": str(caminho_print),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Abre o Chrome instalado e navega para uma URL pública.")
    parser.add_argument("url", type=str, help="URL a visitar")
    parser.add_argument("--visivel", action="store_true", help="Abrir janela visível em vez de headless")
    args = parser.parse_args()

    resultado = navegar(args.url, visivel=args.visivel)
    print(f"URL visitada: {resultado['url']}")
    print(f"Título da página: {resultado['titulo']}")
    print(f"Trecho do conteúdo: {resultado['trecho_texto'][:150]}...")
    print(f"Screenshot salvo em: {resultado['screenshot']}")
