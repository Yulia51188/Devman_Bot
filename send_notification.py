import requests
import os
from requests.exceptions import ReadTimeout, ConnectionError, HTTPError
from dotenv import load_dotenv
from time import sleep
import telegram
from telegram.error import TimedOut, NetworkError, TelegramError
import logging
from logging import FileHandler


SLEEP_TIMEOUT = 30


def send_long_polling_request(token, last_timestamp, timeout=100):
    url_long_polling = "https://dvmn.org/api/long_polling/"

    headers = {
        "Authorization": f"Token {token}"
    }
    params = {
        "timestamp": last_timestamp,
    }
    if last_timestamp:
        response = requests.get(
            url_long_polling, 
            headers=headers,
            params=params,
            timeout=timeout
        )
    else:
        response = requests.get(
            url_long_polling, 
            headers=headers,
            timeout=timeout
        )        
    response.raise_for_status()
    response_data = response.json()
    if "error" in response_data.keys():
        raise HTTPError(f"Error in response with status 200: "
            f"{response_data['error']}")  
    return response_data


def send_notification(results, token, user_id, name="студент"):
    bot = telegram.Bot(token=token)
    greeting = f"Привет, {name}! Твоя работа вернулась с проверки.\n\n"  
    dvmn_base_url = "https://dvmn.org"  
    for result in results:    
        lesson_info = f"Задача:\n{result['lesson_title']}.\n\n"
        if result['is_negative']:
            result_message = "К сожалению, код нуждается в доработке, "
        else:
            result_message = f"Отличный код! Переходи к следующей задаче: "
        url_info = f"{dvmn_base_url}{result['lesson_url']}"
        message = ''.join([greeting, lesson_info, result_message,url_info])
        response = bot.send_message(
            user_id, 
            message
        )


class TelegramLogsHandler(FileHandler):
                        
    def __init__(self, token, admin_id, filename='disconnested.log'):
        self.log_bot = telegram.Bot(token=token)
        self.admin_id = admin_id
        self.filename = filename
        super(FileHandler, self).__init__()
                        
    def emit(self, record):
        log_message = self.format(record)
        try:
            self.log_bot.send_message(self.admin_id, log_message)
        except TelegramError as error:
            with open(self.filename, 'a') as _file_handler:
                _file_handler.write(f'{log_message}\n')


def create_logger(logger_name, token, admin_id):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = TelegramLogsHandler(token, admin_id)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(filename)s: '
        '%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def main(): 
    load_dotenv()
    dvmn_token = os.getenv("DVMN_API_TOKEN")
    telegram_token =  os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_user_id = os.getenv("TELEGRAM_USER_ID")
    telegram_admin_id = os.getenv("TELEGRAM_ADMIN_ID")
    telegram_user_name = os.getenv("TELEGRAM_USER_NAME")
    last_timestamp = None
    logger = create_logger('telegram_logger', telegram_token, 
        telegram_admin_id)
    logger.info("Bot started!")
    while True:
        try:
            response = send_long_polling_request(
                dvmn_token, 
                last_timestamp
            )          
            if response["status"] == "found":
                send_notification(
                    response["new_attempts"], 
                    telegram_token, 
                    telegram_user_id, 
                    name=telegram_user_name
                )
                last_timestamp = response["last_attempt_timestamp"]
            if response["status"] == "timeout":
                last_timestamp = response["timestamp_to_request"]
        except ReadTimeout as error:
            pass
        except (ConnectionError, HTTPError) as error:
            logger.warning(error, exc_info=True)
            sleep(SLEEP_TIMEOUT)
        except (NetworkError, TimedOut) as error:
            logger.warning(error, exc_info=True)
            sleep(SLEEP_TIMEOUT)
        except Exception as error:
            logger.error(error, exc_info=True)


if __name__=='__main__':
    main()
