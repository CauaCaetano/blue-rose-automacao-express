"""
Utilitário — captura de tela.

Tira um screenshot da tela inteira e salva em logs/screenshots/ com nome
baseado em timestamp. Não interage com nada, só captura.

Uso:
    python screenshot.py [--prefixo nome]
"""

import argparse
from datetime import datetime
from pathlib import Path
from PIL import ImageGrab

PASTA_SAIDA = Path(__file__).resolve().parent.parent / "logs" / "screenshots"


def capturar(prefixo: str = "screenshot") -> Path:
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = PASTA_SAIDA / f"{prefixo}_{timestamp}.png"
    imagem = ImageGrab.grab()
    imagem.save(caminho)
    return caminho


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Captura a tela inteira e salva em logs/screenshots/.")
    parser.add_argument("--prefixo", type=str, default="screenshot", help="Prefixo do nome do arquivo")
    args = parser.parse_args()

    caminho = capturar(args.prefixo)
    print(f"Screenshot salvo em: {caminho}")
    print(f"Tamanho: {caminho.stat().st_size} bytes")
