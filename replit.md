# tigraoWeather

Bot de previsão do tempo para Telegram usando aiogram 3.27 + Open-Meteo.

## Visão geral do projeto

- **Linguagem:** Python 3.12
- **Stack:** aiogram 3.27, aiohttp, aiosqlite (SQLite), Pillow, Open-Meteo (sem API key)
- **Entrada:** `python -m app.main`
- **Estrutura:**
  - `app/main.py` — inicialização do bot, dispatcher e routers
  - `app/handlers/` — handlers (start, weather, inline, health)
  - `app/services/` — serviços (weather, geocoding, cache, http client, etc.)
  - `app/keyboards/` — teclados inline
  - `app/middlewares/` — middleware de erro
  - `app/utils/` — utilitários (formatação, wmo, rate limit, etc.)
  - `app/database.py` — SQLite (cache e localizações de usuário)
- **Variáveis:** `BOT_TOKEN` (token do @BotFather)

## Preferências do usuário

- O bot é executado em produção no **Railway**, NÃO neste ambiente Replit.
- Não configurar workflow para rodar o bot aqui nem usar o `BOT_TOKEN` neste ambiente.
- Usar o Replit apenas para trabalho no código.
