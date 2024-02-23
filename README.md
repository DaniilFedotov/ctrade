## Trading bot Ctrade
Ctrade is crypto trading bot written in Python. The project includes the following applications:
* backend;
* tg_bot;
* trading.

The backend is Django application with web interface, API and database with information about transactions and trading bots.
Web interface allows check the statistic in comfortable format.
 
The tg_bot is Telegram bot, which allows to control running trading bot and to get statistic about last transactions.

The trading includes trading bot infrastructure such as strategies, settings and algorithms.
Trading bot works with crypto exchanges through API and connect with database through API of backend application.