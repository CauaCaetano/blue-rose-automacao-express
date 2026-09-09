"""
Exemplo de portfolio — Relatório automático a partir de uma planilha de vendas.

Lê um CSV de vendas (colunas: data, produto, categoria, valor) e gera um
resumo: total geral, total por categoria e total por mês. Exporta o resumo
para um novo CSV. Pensado como demo: "eu automatizo esse relatório que você
faz manualmente toda semana/mês".

Uso:
    python relatorio_vendas.py vendas.csv [--saida resumo.csv]

Formato esperado do CSV de entrada (cabeçalho obrigatório):
    data,produto,categoria,valor
    2026-09-01,Camiseta P,Roupas,49.90
    2026-09-02,Caneca,Casa,29.90

Dependências: nenhuma (só biblioteca padrão do Python).
"""

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def carregar_vendas(caminho: Path):
    # utf-8-sig: lida com CSVs que vêm com BOM (comum em exportações do Excel
    # no Windows), sem quebrar o nome da primeira coluna.
    with caminho.open(newline="", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f)
        return [linha for linha in leitor]


def gerar_resumo(vendas):
    total_geral = 0.0
    por_categoria = defaultdict(float)
    por_mes = defaultdict(float)

    for linha in vendas:
        valor = float(linha["valor"])
        total_geral += valor
        por_categoria[linha["categoria"]] += valor
        mes = linha["data"][:7]  # "AAAA-MM"
        por_mes[mes] += valor

    return total_geral, por_categoria, por_mes


def imprimir_resumo(total_geral, por_categoria, por_mes):
    print(f"\nTotal geral: R${total_geral:,.2f}\n")

    print("Por categoria:")
    for categoria, valor in sorted(por_categoria.items(), key=lambda x: -x[1]):
        print(f"  {categoria:<20} R${valor:,.2f}")

    print("\nPor mês:")
    for mes, valor in sorted(por_mes.items()):
        print(f"  {mes:<10} R${valor:,.2f}")


def salvar_resumo(caminho: Path, total_geral, por_categoria, por_mes):
    with caminho.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["tipo", "chave", "valor"])
        escritor.writerow(["total_geral", "-", f"{total_geral:.2f}"])
        for categoria, valor in por_categoria.items():
            escritor.writerow(["categoria", categoria, f"{valor:.2f}"])
        for mes, valor in por_mes.items():
            escritor.writerow(["mes", mes, f"{valor:.2f}"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera relatório resumido a partir de um CSV de vendas.")
    parser.add_argument("entrada", type=str, help="Caminho do CSV de vendas")
    parser.add_argument("--saida", type=str, default="resumo.csv", help="Caminho do CSV de saída (padrão: resumo.csv)")
    args = parser.parse_args()

    caminho_entrada = Path(args.entrada).expanduser().resolve()
    if not caminho_entrada.is_file():
        raise SystemExit(f"Arquivo não encontrado: {caminho_entrada}")

    vendas = carregar_vendas(caminho_entrada)
    total_geral, por_categoria, por_mes = gerar_resumo(vendas)
    imprimir_resumo(total_geral, por_categoria, por_mes)

    caminho_saida = Path(args.saida).expanduser().resolve()
    salvar_resumo(caminho_saida, total_geral, por_categoria, por_mes)
    print(f"\nResumo salvo em: {caminho_saida}")
