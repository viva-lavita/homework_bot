import os
from time import time

from dotenv import load_dotenv
from typing import Union, Final, Optional
import logging
from telegram import Bot

load_dotenv()


PRACTICUM_TOKEN: Final = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN: Final = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID: Final = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD: int = 600
ENDPOINT: str = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS: dict = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

START, FAIL, OK = ' start', ' FAIL', ' done'
CHECK_ENV = 'Пероверка переменных окружения,'


def check_tokens() -> Optional[bool]:
    """Проверка доступности переменных окружения."""
    logging.info(CHECK_ENV, START)
    tokens = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    for token in tokens:
        if token:
            continue
        logging.critical(CHECK_ENV, FAIL)
        raise EnvironmentError
    logging.info(CHECK_ENV, OK)
    return True




def send_message(bot, message):
    ...


def get_api_answer(timestamp):
    ...


def check_response(response):
    ...


def parse_status(homework):
    ...

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""

    ...

    bot = Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    ...

    while True:
        try:

            ...

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
        ...


if __name__ == '__main__':
    main()
