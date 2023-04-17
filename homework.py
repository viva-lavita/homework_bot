import logging.config
import requests
import requests.exceptions as ex
import time
from http import HTTPStatus

import telegram
from typing import Optional

import constants as c
from constants import ENDPOINT, HEADERS, HOMEWORK_VERDICTS, RETRY_PERIOD
from tokens import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, PRACTICUM_TOKEN


def check_tokens() -> Optional[bool]:
    """Проверка доступности переменных окружения."""
    logging.debug(f'{c.CHECK_ENV} start')
    tokens: dict = {'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
                    'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
                    'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID}
    for token_name, token in tokens.items():
        if token:
            continue
        logging.critical(
            f'{c.CHECK_ENV}, FAIL! {token_name}, {c.PROGRAM_STOPPED}'
        )
        raise EnvironmentError
    logging.info(f'{c.CHECK_ENV} ...OK')
    return True


def send_message(bot: telegram.Bot, message: str) -> None:
    """Отправка сообщения в чат Telegram."""
    logging.debug(f'{c.POST_CHAT} start')
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info(f'{c.POST_CHAT} ...OK')
    except telegram.error.TelegramError as err:
        logging.error(f'{c.POST_CHAT} FAIL!, {err}')


def get_api_answer(timestamp: int) -> Optional[dict]:
    """Получение через API пакета с домашними работами."""
    logging.debug(f'{c.GET_HOMEWORKS} start')
    try:
        response = requests.get(url=ENDPOINT,
                                headers=HEADERS,
                                params={'from_date': timestamp},
                                timeout=10)
        if response.status_code != HTTPStatus.OK:
            raise ex.HTTPError
        logging.info(f'{c.GET_HOMEWORKS} OK')
        return response.json()
    except ex.HTTPError(response) as err:
        logging.error(f'{c.GET_HOMEWORKS} FAIL!, {err}')
    except ex.RequestException as err:
        logging.error(f'{c.GET_HOMEWORKS} FAIL!, {err}', exc_info=True)
        logging.warning


def check_response(response) -> Optional[bool]:
    """Проверяет ответ API на соответствие документации."""
    logging.debug(f'{c.CHECK_API_RESPONSE} start')
    if not isinstance(response, dict):
        raise TypeError
    if 'homeworks' not in response:
        raise ValueError
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError
    logging.debug(f'{c.CHECK_API_RESPONSE} OK')
    return True


def parse_status(homework) -> Optional[str]:
    """.
    Извлекает из информации о конкретной домашней
    работе статус этой работы.
    """
    logging.debug(f'{c.GET_STATUS_HOMEWORK} start')
    # AssertionError: Не найдена переменная `HOMEWORK_VERDICTS`.
    # Не удаляйте и не переименовыв... - Пайтест...
    # HOMEWORK_VERDICTS: dict[str, str] = {
    #     'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    #     'reviewing': 'Работа взята на проверку ревьюером.',
    #     'rejected': 'Работа проверена: у ревьюера есть замечания.'
    # }
    try:
        homework_name = homework['homework_name']
        verdict = HOMEWORK_VERDICTS[homework['status']]
        logging.info(f'{c.GET_STATUS_HOMEWORK} OK')
        return c.HOMEWORK_STATUS_CHANGE.format(homework_name, verdict)
    except Exception as err:
        logging.error(f'{c.GET_STATUS_HOMEWORK} FAIL!, {err}', exc_info=True)
        raise KeyError


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
            logging.error(f'{c.MAIN_LOGIC_BOT} FAIL!, {error}', exc_info=True)
        if last_message != message:
            send_message(bot, message)
            last_message: str = message
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.config.fileConfig('log_config.ini')
    logging = logging.getLogger()
    main()
