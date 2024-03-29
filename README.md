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
You can set up a Telegram bot account via @BotFather.

To use the trading bot you need to deploy containers. To do this you need
to download Docker. For Linux, you can use the following commands.

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
After launching the container network, you need to import the initial settings into the database.
To do this, enter the command in a separate terminal:
```sh
sudo docker exec backend python manage.py importsettings
```

You can open the web interface at http://localhost:8000/.

The following pages are currently available: Home, Deals, Traders.
The Home page contains information about the strategy and instructions for setting up a trading bot.
Transactions opened during trading will be posted on the Deals page. Statistics of created trading
bots will be available in the Traders page.

Telegram bot is used to configure a trading bot, manage it and obtain trading statistics.

The following commands are available for the Telegram bot:
* `/start x` - start existing trading bot with id x;
* `/stop x` - stop trading bot with id x;
* `/revenue x` - get revenue for the last x trades (default - 5);
* `/daily` - get revenue for today;
* `/yesterday` - get revenue for yesterday;
* `/id` - get the id of a running bot;
* `/tickers` - get available tickers;
* `/grids` - get available grids (last created);
* `/grids x` - get grid from id x;
* `/grids a b c d e` - create a grid with the following parameters:
   
  a - bottom, b - top, c - number of levels (from 6 to 40), d - deposit, e - ticker id;
* `/traders` - get available trading accounts (last created);
* `/traders x` - get trading account from id x;
* `/traders a b` - create a trading account with the following parameters:

  a - exchange name (for example - bybit), b - grid id;
* `/help` - get help message.

### What is working at the moment

The web interface is now fully functional. The Telegram bot is also fully functional. 
Currently, only the grid trading strategy works. It is planned to implement other strategies in
the future.

Work is underway to optimize the code. A module for analyzing the volatility of cryptocurrencies
is being developed. He will help you choose a coin for trading using a bot.
