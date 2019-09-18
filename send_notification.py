import requests
import os
from pprint import pprint
from requests.exceptions import ReadTimeout, ConnectionError
from dotenv import load_dotenv
from time import sleep
import telegram
from telegram.error import TimedOut, NetworkError


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
    return response


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


def main(): 
    load_dotenv()
    dvmn_token = os.getenv("DVMN_API_TOKEN")
    telegram_token =  os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_user_id = os.getenv("TELEGRAM_USER_ID")
    telegram_user_name = os.getenv("TELEGRAM_USER_NAME")
    last_timestamp = None
    while True:
        try:
            response = send_long_polling_request(
                dvmn_token, 
                last_timestamp
            )
            response_data = response.json()
            if response_data["status"] == "found":
                send_notification(
                    response_data["new_attempts"], 
                    telegram_token, 
                    telegram_user_id, 
                    name=telegram_user_name
                )
                last_timestamp = response_data["last_attempt_timestamp"]
            if response_data["status"] == "timeout":
                last_timestamp = response_data["timestamp_to_request"]
        except ReadTimeout as error:
            pass
        except ConnectionError as error:
            print(f"WARNING:{error}")
            sleep(SLEEP_TIMEOUT)
        except (NetworkError, TimedOut) as error:
            print(f"WARNING:{error}")
            sleep(SLEEP_TIMEOUT)


if __name__=='__main__':
    main()