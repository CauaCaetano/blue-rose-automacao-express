"""
Utilitário — abrir um aplicativo local e confirmar que a janela existe.

Usa pywinauto (UI Automation) para abrir o app e ler o título da janela —
não clica em nada dentro do app, só confirma que abriu. Por padrão fecha o
app no final do teste.

Busca a janela pelo conjunto de janelas de topo do Desktop (não pelo PID do
processo iniciado) porque vários apps modernos do Windows 11 (Notepad,
Calculadora etc.) são empacotados como MSIX: o processo que o SO retorna ao
iniciar não é o mesmo que acaba dono da janela, então rastrear por PID falha.

Uso:
    python abrir_app.py notepad.exe [--nao-fechar]
"""

import argparse
import subprocess
import time
from pywinauto import Desktop


def _janelas_visiveis_por_handle():
    return {
        w.handle: w
        for w in Desktop(backend="uia").windows()
        if w.is_visible() and w.window_text().strip()
    }


def abrir_e_confirmar(comando: str, fechar_no_final: bool = True, tentativas: int = 10):
    handles_antes = set(_janelas_visiveis_por_handle().keys())
    processo = subprocess.Popen(comando)

    janela = None
    for _ in range(tentativas):
        time.sleep(0.5)
        atuais = _janelas_visiveis_por_handle()
        novas = [h for h in atuais if h not in handles_antes]
        if novas:
            janela = atuais[novas[0]]
            break

    if janela is None:
        raise RuntimeError(f"Nenhuma janela nova encontrada após iniciar '{comando}'")

    titulo = janela.window_text()
    classe = janela.friendly_class_name()

    print(f"App iniciado: {comando}")
    print(f"Janela encontrada -> título: '{titulo}' | tipo: {classe}")

    if fechar_no_final:
        try:
            janela.close()
        except Exception:
            processo.kill()
        print("Janela fechada (teste concluído).")

    return titulo, classe


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Abre um app local e confirma a janela via UI Automation.")
    parser.add_argument("comando", type=str, help="Comando/caminho do app a abrir (ex.: notepad.exe)")
    parser.add_argument("--nao-fechar", action="store_true", help="Não fechar o app ao final")
    args = parser.parse_args()

    abrir_e_confirmar(args.comando, fechar_no_final=not args.nao_fechar)
