import logging
# import json
import os
import requests
import requests.exceptions as ex
import time

from dotenv import load_dotenv
# import jsonschema
# from jsonschema.exceptions import ValidationError
import telegram
from typing import Final, Optional


load_dotenv()


PRACTICUM_TOKEN: Final = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN: Final = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID: Final = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD: int = 600
ENDPOINT: str = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS: dict = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS: dict[str, str] = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

START, FAIL, OK = ' start', ' ...FAIL', ' ...done'
UNKNOWN_ERROR: str = '...UNKNOWN_ERROR'
PROGRAM_STOPPED: str = '  Программа принудительно остановлена'
CHECK_ENV: str = 'Пероверка переменных окружения,'
GET_HOMEWORKS: str = 'Получение пакета с домашними работами,'
POST_CHAT: str = 'Отправка сообщения в чат Telegram,'
CHECK_API_RESPONSE: str = 'Проверка ответа API на сооветствие документации,'
GET_STATUS_HOMEWORK: str = 'Получение статуса домашней работы,'
HOMEWORK_STATUS_CHANGE: str = 'Изменился статус проверки работы "{0}". {1}'
MAIN_LOGIC_BOT: str = 'Основная логика работы бота.'


def check_tokens() -> Optional[bool]:
    """Проверка доступности переменных окружения."""
    logging.debug(CHECK_ENV + START)
    tokens: dict = {'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
                    'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
                    'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID}
    for token_name, token in tokens.items():
        if token:
            continue
        logging.critical(f'{CHECK_ENV, FAIL + token_name, PROGRAM_STOPPED}')
        raise EnvironmentError
    logging.info(CHECK_ENV + OK)
    return True


def send_message(bot: telegram.Bot, message: str) -> None:
    """Отправка сообщения в чат Telegram."""
    logging.debug(POST_CHAT + START)
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info(POST_CHAT + OK)
    except telegram.error.TelegramError as err:
        logging.error(f'{POST_CHAT, FAIL, err}')


def get_api_answer(timestamp: int) -> Optional[dict]:
    """Получение через API пакета с домашними работами."""
    logging.debug(GET_HOMEWORKS + START)
    try:
        response = requests.get(url=ENDPOINT,
                                headers=HEADERS,
                                params={'from_date': timestamp},
                                timeout=10)
        # response.raise_for_status()    # у пайтеста нет этого встроенного
        if response.status_code != 200:  # метода библиотеки requests
            raise ex.HTTPError           # проверка на 200 - замена
        logging.info(GET_HOMEWORKS + OK)
        return response.json()
    except ex.HTTPError(response) as err:
        logging.error(f'{GET_HOMEWORKS, FAIL, err}')
    except ex.RequestException as err:
        logging.error(f'{GET_HOMEWORKS, FAIL, err}', exc_info=True)


# Пайтест сказал, что не знает что такое jsonschema...
# Просьба по возможности краем глаза посмотреть и его.
def check_response(response) -> Optional[bool]:
    """Проверяет ответ API на соответствие документации."""
    logging.debug(CHECK_API_RESPONSE + START)
    # try:
    #     with open('schema.json') as f:
    #         SCHEMA = json.load(f)
    #     jsonschema.validate(response, SCHEMA)
    #     logging.info(CHECK_API_RESPONSE + OK)
    #     return True
    # except Exception as err:
    #     logging.error(f'{CHECK_API_RESPONSE, FAIL, err}', exc_info=True)
    if not isinstance(response, dict):
        raise TypeError
    if 'homeworks' not in response:
        raise ValueError
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError
    logging.debug(CHECK_API_RESPONSE + OK)
    return True


def parse_status(homework) -> Optional[str]:
    """.
    Извлекает из информации о конкретной домашней
    работе статус этой работы.
    """
    logging.debug(GET_STATUS_HOMEWORK + START)
    try:
        homework_name = homework['homework_name']
        verdict = HOMEWORK_VERDICTS[homework['status']]
        logging.info(GET_STATUS_HOMEWORK + OK)
        return HOMEWORK_STATUS_CHANGE.format(homework_name, verdict)
    except Exception as err:
        logging.error(f'{GET_STATUS_HOMEWORK + FAIL, err}', exc_info=True)
        raise KeyError  # Пайтест попросил отпустить ошибку дальше


def main() -> None:
    """Основная логика работы бота."""
    check_tokens()
    timestamp: int = int(time.time())
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    last_status, last_message, message = None, None, None
    while True:
        try:
            response: Optional[dict] = get_api_answer(timestamp)
            check_response(response)
            if response['homeworks']:
                homework: dict = response['homeworks'][0]
                if last_status != homework['status']:
                    message: str = parse_status(homework)
                    timestamp: int = response['current_date']
        except Exception as error:
            message: str = f'Сбой в работе программы: {error}'
            logging.error(f'{MAIN_LOGIC_BOT, FAIL, error}', exc_info=True)
        if last_message != message:
            send_message(bot, message)
            last_message: str = message
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, %(message)s',
        filename='main.log', encoding='UTF-8',
    )
    main()
