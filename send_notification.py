import requests
import os
from pprint import pprint
from requests.exceptions import ReadTimeout, ConnectionError
from dotenv import load_dotenv
from time import sleep
import telegram


def send_long_polling_request(token, timeout, last_timestamp):
# url = "https://dvmn.org/api/user_reviews/"
    url_long_polling = "https://dvmn.org/api/long_polling/"

    headers = {
        "Authorization": f"Token {token}"
    }
    params = {
        "timestamp": last_timestamp,
    }
    if last_timestamp:
        print(f"\nSend request with {last_timestamp}...")
        response = requests.get(
            url_long_polling, 
            headers=headers,
            params=params,
            timeout=timeout
        )
    else:
        print(f"\nSend request...")
        response = requests.get(
            url_long_polling, 
            headers=headers,
            timeout=timeout
        )        
    return response

def request_in_loop(dvmn_token, timeout):
    last_timestamp = None
    while True:
        try:
            response = send_long_polling_request(dvmn_token, timeout, last_timestamp)
            response_data = response.json()
            print(response_data["status"])
            if response_data["status"] == "found":
                last_timestamp = response_data["last_attempt_timestamp"]
            if response_data["status"] == "timeout":
                last_timestamp = response_data["timestamp_to_request"]
            pprint(response.json())
        except ReadTimeout as error:
            print(f"Timeout Error occured: {error}")
        except ConnectionError as error:
            print(error)
            sleep(timeout)


def main(): 
    load_dotenv()
    dvmn_token = os.getenv("DVMN_API_TOKEN")
    timeout = 5
    # request_in_loop(dvmn_token, timeout)
    telegram_token =  os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_user_id = os.getenv("TELEGRAM_USER_ID")
    bot = telegram.Bot(token=telegram_token)
    print(bot.get_me())
    response = bot.send_message(
        telegram_user_id, 
        f"Уже пора, диктант через 11 минут!"
    )
    print(response)


if __name__=='__main__':
    main()