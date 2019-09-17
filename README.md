# Devman_Bot

The program requests for the availability of the verified work of the [Devman API](https://dvmn.org/api/docs/) and sends a notification to Telegram in case the task returns from the check.

# How to install
The script uses enviroment file with Devman and Telegram authorization data. The file '.env' must include following data:
- DVMN_API_TOKEN, individual token of Devman API
- TELEGRAM_BOT_TOKEN, Telegram bot token
- TELEGRAM_USER_ID, an ID of a Telegram user who get the notification
- TELEGRAM_USER_NAME, a name of a Telegram user who get the notification

Python 3 should be already installed. Then use pip3 (or pip) to install dependencies:

```bash
pip3 install -r requirements.txt
```

# How to launch
The Example of launch in Ubuntu is:

```bash
$ python3 send_notification.py 
```

# Project Goals

The code is written for educational purposes on online-course for web-developers dvmn.org, module [Chat Bots with Python](https://dvmn.org/modules/chat-bots/lesson/devman-bot/#review-tabs).

