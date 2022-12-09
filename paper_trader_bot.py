import logging
import os

import random
import requests

from bs4 import BeautifulSoup
from telegram.ext import CommandHandler, Updater

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
TOKEN_NAMES = [
    'TOKEN',
]
TOKEN_MISSING = (
    'Environment variable missing: "{token}".'
)
CHECK_TOKENS_FALSE = 'Данные авторизации недоступны.'
URL = 'https://paper-trader.frwd.one/'
ERROR_MESSAGE = f'An error occured during request to {URL}: '
NO_ARGS_MESSAGE = 'Please, specify the trading pair.'
START_UP_MESSAGE = ('Hi, {name}. Send me a trading pair '
                    '(for example: "/get_chart BTCUSDT") '
                    'and I will send you the generated chart')
TIMEFRAMES = ['5m', '15m', '1h', '4h', '1d', '1w', '1M']


def get_picture(pair: str) -> str:
    '''Gets picture from result page.'''
    form_data = {
        'pair': pair,
        'timeframe': random.choice(TIMEFRAMES),
        'candles': random.randint(1, 1000),
        'ma': random.randint(1, 10) * 10,
        'tp': random.randint(1, 15),
        'sl': random.randint(1, 15),
    }
    try:
        response = requests.post(URL, data=form_data)
    except Exception as error:
        logging.error(ERROR_MESSAGE + error)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    return images[0].get('src').replace(
        '.',
        'https://paper-trader.frwd.one',
        1,
    )


def send_picture(update, context):
    '''Sends parces picture URL to chat,'''
    chat = update.effective_chat
    if not context.args:
        context.bot.send_message(
            chat_id=chat.id,
            text=NO_ARGS_MESSAGE,
        )
    else:
        context.bot.send_photo(chat.id, get_picture(context.args[0]))


def wake_up(update, context):
    '''Start a bot.'''
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat.id,
        text=START_UP_MESSAGE.format(name=name)
    )


def check_tokens():
    '''Checks environment variables.'''
    missing_tokens = [name for name in TOKEN_NAMES if not globals()[name]]
    if not missing_tokens:
        return True
    logging.critical(TOKEN_MISSING.format(token=missing_tokens))
    return False


def main():
    '''Gets chat updated and reacts accordingly.'''
    if not check_tokens():
        raise ValueError(CHECK_TOKENS_FALSE)
    updater = Updater(token=TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('get_chart', send_picture))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
