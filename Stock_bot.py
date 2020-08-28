# requires python modules LXML, Yfinance, and python-telegram-bot

import yfinance as yf
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_data(ticker_name):
    apple_data = yf.Ticker(ticker_name)

    data = apple_data.info
    return data


def get_price(ticker_name):
    current_price = get_data(ticker_name)['bid']

    return f' The current price of {ticker_name.upper()} is ${current_price}'


def get_summary(ticker_name):
    current_data = get_data(ticker_name)
    day_high, day_low, current_price = current_data['dayHigh'], current_data['dayLow'], current_data['bid']

    return f' Day Summary for {ticker_name.upper()}:\nDay High: {day_high}\nDay Low: {day_low}\nCurrent Price: {current_price}'


def get_grout_worth():
    apple_ticker = 'AAPL'
    grout_worth = get_data(apple_ticker)['bid'] * 100

    return f"Gunt's Apple shares are worth ${round(grout_worth)}"


def get_aapl():
    apple_ticker = 'AAPL'
    current_price = get_data(apple_ticker)['bid']

    return f' The current price of AAPL is ${current_price}'


def show_help():
    help_message = ("Help Menu\n"
                    "/aapl - will display the current price of AAPL\n"
                    "/stock <ticker> - will display the current price of a share of that companies stock\n"
                    "/worth - will display the total price of AAPL * 60\n"
                    "/summary <ticker> - will display a basic summary of today's prices of that companies stock\n")

    return help_message


def stock(update, context):
    """Sends current price of apple share when command /price is issued"""
    update.message.reply_text(get_price(update.message.text.replace('/stock ', '')))


def worth(update, context):
    """Sends current apple share price * 100 when command /worth is issued"""
    update.message.reply_text(get_grout_worth())


def summary(update, context):
    """Sends the current summary for the day when the command /summary is issued"""
    update.message.reply_text(get_summary(update.message.text.replace('/summary ', '')))


def aapl(update, context):
    """Sends current price of apple share when command /price is issued"""
    update.message.reply_text(get_aapl())


def help_command(update, context):
    """Displays help menu when command /help is issued"""
    update.message.reply_text(show_help())


def main():
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("stock", stock))
    dp.add_handler(CommandHandler("worth", worth))
    dp.add_handler(CommandHandler("summary", summary))
    dp.add_handler(CommandHandler("aapl", aapl))
    dp.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
