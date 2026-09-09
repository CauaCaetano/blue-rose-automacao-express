# Automação — SURVIVE400

Utilitários de automação operacional, seguindo a ordem de prioridade definida
no protocolo (item 4 do adendo de autonomia):

```
API > DOM/browser automation > UI Automation > Power Automate Desktop
    > mouse/teclado > cliques por coordenadas
```

## Ferramentas usadas

| Ferramenta | Papel | Por quê |
|---|---|---|
| **Playwright** (Python) | Automação de navegador via DOM | Mais confiável que clique por coordenada — opera nos elementos da página, não na posição da tela. Usa o Chrome já instalado (`channel="chrome"`), sem baixar Chromium extra. |
| **pywinauto** (backend UIA) | Automação de apps Windows via UI Automation | Lê/interage com janelas pelo nome/controle, não por posição de pixel — muito mais estável. |
| **Pillow** | Captura de tela | `ImageGrab` já cobre o caso de uso sem dependência pesada. |
| **Power Automate Desktop** | Fluxos recorrentes já gravados por humano | Já vem instalado no Windows; reservado para fluxos que você grava e eu só disparo, dentro de limites definidos. |

## O que NÃO foi instalado (e por quê)

- **pyautogui / keyboard / mouse (cliques por coordenada bruta)** — é o último
  recurso na ordem de prioridade; Playwright + pywinauto cobrem os casos de
  uso atuais com mais confiabilidade. Instalar depois, só se aparecer um app
  sem API/DOM/UIA acessível.
- **OCR (pytesseract + Tesseract)** — nenhuma tarefa até agora precisa "ler"
  texto de uma imagem; UI Automation e DOM já expõem o texto diretamente.
  Fica reservado para quando for realmente necessário.
- **Node.js / Selenium** — Playwright em Python já cobre a necessidade de
  automação de navegador sem precisar de outro runtime.

## Scripts

- `screenshot.py` — tira um screenshot da tela inteira e salva em
  `logs/screenshots/`.
- `abrir_app.py` — abre um aplicativo local e confirma que a janela existe
  (via pywinauto), sem clicar em nada dentro dele.
- `navegador.py` — abre o Chrome já instalado via Playwright, navega para uma
  URL, confirma o título/conteúdo da página e salva um screenshot.

## Regras de segurança (fixas, não mudam com o nível de autonomia)

- Nunca abrir apps de banco, carteira digital ou app de pagamento.
- Nunca preencher campo de login, senha, CPF, cartão ou dado de pagamento.
- Nunca clicar em botão de "comprar", "pagar", "enviar Pix", "transferir" ou
  equivalente.
- Nunca enviar mensagem real para uma pessoa real sem revisão sua.
- Nunca criar conta real em nenhuma plataforma sem sua aprovação explícita.
- Toda execução destes scripts é registrada em `logs/log.md`.
