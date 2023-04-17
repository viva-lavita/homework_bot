# import tokens


# RETRY_PERIOD: int = 600
# ENDPOINT: str = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
# HEADERS: dict = {'Authorization': f'OAuth {tokens.PRACTICUM_TOKEN}'}

# HOMEWORK_VERDICTS: dict[str, str] = {
#     'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
#     'reviewing': 'Работа взята на проверку ревьюером.',
#     'rejected': 'Работа проверена: у ревьюера есть замечания.'
# }

# Закоментила, не удаляю, раскоментю после ревью.

PROGRAM_STOPPED: str = '  Программа принудительно остановлена'
CHECK_ENV: str = 'Пероверка переменных окружения,'
GET_HOMEWORKS: str = 'Получение пакета с домашними работами,'
POST_CHAT: str = 'Отправка сообщения в чат Telegram,'
CHECK_API_RESPONSE: str = 'Проверка ответа API на сооветствие документации,'
GET_STATUS_HOMEWORK: str = 'Получение статуса домашней работы,'
HOMEWORK_STATUS_CHANGE: str = 'Изменился статус проверки работы "{0}". {1}'
MAIN_LOGIC_BOT: str = 'Основная логика работы бота.'
