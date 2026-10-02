# BLUE ROSE: automação, sistemas e sites para negócios locais

Site: https://cauacaetano.github.io/blue-rose-automacao-express/ (inglês: `clinicas-en.html`)

## O que tem neste repositório

| Pasta / arquivo | O que é |
|---|---|
| `index.html`, `clinicas-en.html` | Página inicial (PT e EN): hub "Experimente", simulador de automações, cases, preços e contato |
| `projetos.html`, `projects-en.html` | Cases com problema, solução, fluxo, testes e a demonstração embutida |
| `laboratorio.html`, `lab-en.html` | Os scripts de `portfolio/` rodando no navegador (Pyodide em um Web Worker) |
| `demos/stockmaster/` | Build do StockMaster em modo demonstração (React + API no navegador) |
| `exemplos*.html`, `demo-*.html` | Seis sites de exemplo por nicho (nomes e preços ilustrativos) |
| `css/site.css`, `js/site.js`, `js/lab*.js` | Sistema visual e comportamento |
| `js/contato.js`, `js/leads-config.js` | Contato codificado e destino opcional do formulário (Supabase, só inserção) |
| `portfolio/` | Automações em Python com testes (`python -m unittest test_portfolio`) |

## Projetos apresentados

- **StockMaster**: controle de estoque em FastAPI, MongoDB e React ([repositório](https://github.com/CauaCaetano/App-Controle-de-Estoque), [demo](https://cauacaetano.github.io/blue-rose-automacao-express/demos/stockmaster/)).
- **Automações de WhatsApp**: qualificador de leads e recuperação de PIX (`portfolio/`).
- **Sites para negócios locais**: os seis exemplos, navegáveis por nicho e dispositivo.
- **Laboratório**: gerador de descrições com IA, relatório de vendas, organizador de arquivos.

## Princípios

- Nada é apresentado como trabalho de cliente pagante, depoimento ou resultado financeiro: são projetos próprios, construídos e testados.
- O site não usa cookies, analytics nem fontes de terceiros (Geist é servida daqui, licença OFL em `fonts/`).
- A demonstração da página inicial é uma simulação no navegador com as mesmas regras dos scripts de `portfolio/`; nenhuma mensagem é enviada.

## Rodar localmente

```bash
python -m http.server 8000
```

Depois abra http://127.0.0.1:8000.
