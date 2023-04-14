import json
import os
from time import time
import requests
import requests.exceptions as ex

from dotenv import load_dotenv
import jsonschema
from jsonschema.exceptions import ValidationError
import logging
from telegram import Bot, error
from typing import Final, Optional


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

START, FAIL, OK = ' start', ' ...FAIL', ' ...done'
UNKNOWN_ERROR = '...UNKNOWN_ERROR'
PROGRAM_STOPPED = 'Программа принудительно остановлена'
CHECK_ENV = 'Пероверка переменных окружения,'
GET_HOMEWORKS = 'Получение пакета с домашними работами,'
POST_CHAT = 'Отправка сообщения в чат Telegram,'
CHECK_API_RESPONSE = 'Проверка ответа API на сооветствие документации,'
GET_STATUS_HOMEWORK = 'Получение статуса домашней работы,'
HOMEWORK_STATUS_CHANGE = 'Изменился статус проверки работы "{0}". {1}'


def check_tokens() -> Optional[bool]:
    """Проверка доступности переменных окружения."""
    logging.info(CHECK_ENV, START)
    tokens = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]  # Словарь?
    for token in tokens:  # name_token, token in tokens.items()
        if token:
            continue
        logging.critical(CHECK_ENV, FAIL, PROGRAM_STOPPED)
        raise EnvironmentError
    logging.debug(CHECK_ENV, OK)
    return True


def send_message(bot: Bot, message: str) -> None:
    """Отправка сообщения в чат Telegram."""
    logging.info(POST_CHAT, START)
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(POST_CHAT, OK)    # прописать пользовательский класс
    except error.TelegramError as err:
        logging.error(POST_CHAT, FAIL, err)


def get_api_answer(timestamp: int) -> Optional[dict]:
    """Получение через API пакета с домашними работами."""
    logging.info(GET_HOMEWORKS, START)
    try:
        response = requests.get(url=ENDPOINT,
                                headers=HEADERS,
                                params={'from_date': timestamp},
                                timeout=10)
        response.raise_for_status()
        logging.debug(GET_HOMEWORKS, OK)
        return response.json()
    except ex.HTTPError(response) as err:
        logging.error(GET_HOMEWORKS, FAIL, err)
    except (ex.ConnectionError, ex.Timeout) as err:
        logging.error(GET_HOMEWORKS, FAIL, err)
    except ex.RequestException as err:
        logging.error(GET_HOMEWORKS, UNKNOWN_ERROR, err)


def check_response(response) -> Optional[bool]:
    """Проверяет ответ API на соответствие документации."""
    logging.info(CHECK_API_RESPONSE, START)
    try:
        with open('schema.json') as f:
            SCHEMA = json.load(f)
        jsonschema.validate(response, SCHEMA)
        logging.debug(CHECK_API_RESPONSE, OK)
        return True
    except ValidationError as err:
        logging.error(CHECK_API_RESPONSE, FAIL, err)
    except Exception as err:
        logging.error(CHECK_API_RESPONSE, UNKNOWN_ERROR, err)


def parse_status(homework) -> str:
    """
    Извлекает из информации о конкретной домашней
    работе статус этой работы.
    """
    logging.info(GET_STATUS_HOMEWORK, START)
    try:
        if isinstance(homework, dict):
            homework_name = homework['homework_name']
            verdict = HOMEWORK_VERDICTS[homework['status']]
            return HOMEWORK_STATUS_CHANGE.format(homework_name, verdict)
        else:
            raise TypeError
    except (KeyError, TypeError) as err:
        logging.error(GET_STATUS_HOMEWORK, FAIL, err)


def main():
    """Основная логика работы бота."""
    check_tokens()


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


if __name__ == '__main__':
    main()
