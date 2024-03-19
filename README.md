## Trading bot Ctrade
Ctrade is crypto trading bot written in Python. The project includes 
the following applications:
* backend;
* tg_bot;
* trading.

The backend is Django application with web interface, API and database with 
information about transactions and trading bots. Web interface allows check 
the statistic in comfortable format.
 
The tg_bot is Telegram bot, which allows to control running trading bot 
and to get statistic about last transactions.

The trading includes trading bot infrastructure such as strategies, settings
and algorithms. Trading bot works with crypto exchanges through API and connect
with database through API of backend application.

### Disclaimer

This trading bot is for educational only. Author does not accept 
any responsibility for your trading results.

### How to start

Clone the repository:
```sh
git clone https://github.com/DaniilFedotov/ctrade.git
```
Go to the project folder and create a .env file:
```sh
cd ctrade
```
```sh
touch .env
```
Fill the .env file in accordance with the example in .env.example:
```
# Django settings.
SECRET_KEY=XYZ  # Django secret key.
ALLOWED_HOSTS=127.0.0.1,localhost,backend  # Host/domain names that Django site can serve.

# Postgres settings.
POSTGRES_DB=user
POSTGRES_USER=user
POSTGRES_PASSWORD=123
DB_HOST=db
DB_PORT=5432

# Telegram bot settings.
TELEGRAM_TOKEN=XYZ  # Token for working with Telegram Bot API.
TELEGRAM_CHAT_ID=XYZ  # ID of the chat to which the bot should send a message.

# Exchange settings for selected exchange.
BYBIT_API_KEY=XYZ  # API key for Bybit exchange.
BYBIT_SECRET_KEY=XYZ  # Secret key for Bybit exchange.
BINANCE_API_KEY=XYZ  # API key for Binance exchange.
BINANCE_SECRET_KEY=XYZ  # Secret key for Binance exchange.
```
You can generate secret key and add your server IP in ALLOWED_HOSTS. 
You can set up a bot account via @BotFather.

To use the trading bot you need to deploy containers. To do this you need
to download Docker. For Linux you can use the following commands.

Installing console utility curl:
```sh
sudo apt install curl
```
Download the script for installing Docker from the official website:
```sh
curl -fSL https://get.docker.com -o get-docker.sh
```
Run the saved script:
```sh
sudo sh ./get-docker.sh
```
Install the Docker Compose utility:
```sh
sudo apt-get install docker-compose-plugin
```

After installing Docker, you can start a container network with the command:
```sh
sudo docker compose up
```
To get acquainted with the wev interface, you can fill the database with 
test data. To do this, enter the command in a separate terminal:
```sh
sudo docker exec backend python manage.py testimport
```

The following pages are currently available: Deals, Traders.

You can open the web interface at http://localhost:8000/

The following commands are available for the Telegram bot:
* `/start x` - start existing trading bot with id x;
* `/stop x` - stop trading bot with id x;
* `/revenue x` - get revenue for the last x trades (default - 5);
* `/daily` - get revenue for today;
* `/id` - get the id of a running bot;
* `/help` - get help message.

### What is working at the moment
The web interface is now fully functional. The Telegram bot has most of the 
commands implemented, but creating a trading bot is not yet available.
Active work is underway on the trading bot module.

Detailed instructions for creating a trading bot via Telegram bot and setting up
a strategy will be created after completing work on the trading bot module.
