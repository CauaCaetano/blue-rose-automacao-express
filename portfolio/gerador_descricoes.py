"""
Exemplo de portfolio — Gerador automático de descrições de produto.

Demonstra o "esqueleto" de uma automação com IA: entrada estruturada ->
montagem de prompt -> geração de texto -> saída pronta para uso. Hoje a
geração usa um template local (sem depender de nenhuma credencial), mas o
ponto `gerar_com_ia()` é exatamente onde entraria uma chamada real a uma API
de IA (ex.: Claude) quando o cliente tiver uma chave configurada.

Uso:
    python gerador_descricoes.py --nome "Caneca de cerâmica" \\
        --caracteristicas "300ml,cerâmica,vai no microondas" \\
        --publico "presente para escritório"

Dependências: nenhuma (só biblioteca padrão do Python).
"""

import argparse


def montar_prompt(nome: str, caracteristicas: list[str], publico: str) -> str:
    lista = ", ".join(caracteristicas)
    return (
        f"Escreva uma descrição de produto curta e persuasiva para '{nome}'. "
        f"Características: {lista}. Público-alvo: {publico}. "
        f"Tom: vendedor, direto, sem exageros."
    )


def gerar_com_ia(prompt: str) -> str:
    """
    PLACEHOLDER: aqui entraria a chamada real a uma API de IA (ex.: Claude),
    usando a chave do cliente via variável de ambiente — nunca hardcoded.
    Por enquanto, gera um texto simples baseado em template, só para
    demonstrar o pipeline sem depender de credencial nenhuma.
    """
    return (
        f"[Rascunho gerado localmente — troque por chamada de IA real]\n"
        f"Descrição baseada no prompt:\n\"{prompt}\""
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera uma descrição de produto a partir de dados estruturados.")
    parser.add_argument("--nome", required=True, help="Nome do produto")
    parser.add_argument("--caracteristicas", required=True, help="Lista separada por vírgula")
    parser.add_argument("--publico", required=True, help="Público-alvo do produto")
    args = parser.parse_args()

    caracteristicas = [c.strip() for c in args.caracteristicas.split(",")]
    prompt = montar_prompt(args.nome, caracteristicas, args.publico)
    resultado = gerar_com_ia(prompt)

    print("\n--- PROMPT MONTADO ---")
    print(prompt)
    print("\n--- RESULTADO ---")
    print(resultado)
