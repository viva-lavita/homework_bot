import os
from time import time
import requests
import requests.exceptions as ex

from dotenv import load_dotenv
from typing import Final, Optional
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
GET_HOMEWORKS = 'Получение пакета с домашними работами,'
POST_CHAT = 'Отправка сообщения в чат Telegram,'


def check_tokens() -> Optional[bool]:
    """Проверка доступности переменных окружения."""
    logging.info(CHECK_ENV, START)
    tokens = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]  # Словарь?
    for token in tokens:  # name_token, token in tokens.items()
        if token:
            continue
        logging.critical(CHECK_ENV, FAIL)
        raise EnvironmentError
    logging.info(CHECK_ENV, OK)
    return True


def send_message(bot: Bot, message: str) -> None:
    """Отправка сообщения в чат Telegram."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(POST_CHAT, OK)
    except:
        logging.error(POST_CHAT, FAIL)


def get_api_answer(timestamp: int) -> Optional[dict]:
    """Получение через API пакета с домашними работами."""
    logging.info(GET_HOMEWORKS, START)
    try:
        response = requests.get(url=ENDPOINT,
                                headers=HEADERS,
                                params={'from_date': timestamp},
                                timeout=10)
        response.raise_for_status()
        logging.info(GET_HOMEWORKS, OK)
        return response.json()
    except ex.HTTPError as err:    # Попробовать потом в скобки бахнуть все ошибки разом?
        logging.error(GET_HOMEWORKS, FAIL, err)
    except (ex.ConnectionError, ex.Timeout) as err:  # Сетевые проблемы
        logging.error(GET_HOMEWORKS, FAIL, err)
    except ex.RequestException as err:               #  Все остальное
        logging.error(GET_HOMEWORKS, FAIL, err)


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
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
