# BLUE ROSE: automação, sistemas e sites para negócios locais

Site: https://cauacaetano.github.io/blue-rose-automacao-express/ (inglês: `clinicas-en.html`)

## O que tem neste repositório

| Pasta / arquivo | O que é |
|---|---|
| `index.html`, `clinicas-en.html` | Página inicial (PT e EN) com a demonstração ao vivo das automações |
| `projetos.html`, `projects-en.html` | Cases completos: problema, solução, como funciona, tecnologias e testes |
| `exemplos*.html`, `demo-*.html` | Seis sites de exemplo por nicho (nomes e preços ilustrativos) |
| `css/site.css`, `js/site.js` | Sistema visual (Geist, um único azul, tema claro/escuro) e comportamento |
| `js/contato.js` | WhatsApp e e-mail codificados, montados só no navegador |
| `portfolio/` | Automações em Python com testes (`python -m unittest test_portfolio`) |
| `automacao/` | Utilitários internos (captura de tela, navegador, apps do Windows) |

## Projetos apresentados no site

- **Escritório BLUE ROSE**: 14 agentes de IA com aprovação humana ([repositório](https://github.com/CauaCaetano/escritorio-blue-rose)).
- **StockMaster**: controle de estoque em FastAPI, MongoDB e React ([repositório](https://github.com/CauaCaetano/App-Controle-de-Estoque)).
- **Automações de WhatsApp**: qualificador de leads e recuperação de PIX (`portfolio/`).
- **Laboratório**: gerador de descrições com IA, relatório de vendas, organizador de arquivos (`portfolio/`).

## Princípios

- Nada é apresentado como trabalho de cliente pagante, depoimento ou resultado financeiro: são projetos próprios, construídos e testados.
- O site não usa cookies, analytics nem fontes de terceiros (Geist é servida daqui, licença OFL em `fonts/`).
- A demonstração da página inicial é uma simulação no navegador com as mesmas regras dos scripts de `portfolio/`; nenhuma mensagem é enviada.

## Rodar localmente

```bash
python -m http.server 8000
```

Depois abra http://127.0.0.1:8000.
