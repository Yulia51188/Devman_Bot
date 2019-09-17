import requests
import os
from pprint import pprint
from requests.exceptions import ReadTimeout, ConnectionError
from dotenv import load_dotenv
from time import sleep


def send_long_polling_request(token):
# url = "https://dvmn.org/api/user_reviews/"
    url_long_polling = "https://dvmn.org/api/long_polling/"
    print("\nSend request...")
    response = requests.get(
        url_long_polling, 
        headers = {
            "Authorization": f"Token {token}"
        },
        timeout=5
    )
    return response


def main(): 
    load_dotenv()
    token = os.getenv("DVMN_API_TOKEN")
    while True:
        try:
            response = send_long_polling_request(token)
            pprint(response.json())
        except ReadTimeout as error:
            print("Timeout Error occured: {error}")
        except ConnectionError as error:
            print(error)
            sleep(5)


if __name__=='__main__':
    main()