# Marketplace API hanler

## Purpose

This app helps to get information from marketplace API (this project was oriented on API https://openapi.wildberries.ru/statistics/api/ru/#tag/Statistika), save it into the database and push the reports to the Telegram bot.


## Installation and launch


### Bot creation

- First, you need to create a new bot in Telegram and retrieve API token.

### Clone the repository

```
git clone git@github.com:Dddarknight/marketplace-api-handler.git
```

Enter the app directory:

```
cd marketplace-api-handler
```

### Environment config

- You have to fill .env file in /deploy directory (see .env.example). 
- Additional description:

```
TG_API_TOKEN is your bot API token.
CHAT_ID variable is your user ID in Telegram (to make the bot send reports to you).
API_KEY is your HeaderApiKey to request marketplace API.
REQUESTS_PERIODICITY is information request frequency in seconds.
```

### Launch

- The app is dockerized. Use docker compose to launch it (from the project root).

```
docker compose -f deploy/docker-compose.yml  up --build -d
```

- This command will also launch tests for the app.
