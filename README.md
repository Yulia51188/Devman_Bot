# Devman_Bot

A bot is useful for [Devman](https://dvmn.org/modules/) students. It sends you notification in Telegram chat if the task is verified. 

The bot uses [Devman API](https://dvmn.org/api/docs/) and [python-telegram-bot](https://pypi.org/project/python-telegram-bot/). It supplies long polling requests with duration 100s. It sents error log to administrator's Telegram chat. If there is no connection it saves log to a file 'disconnested.log'.

# How to install
The script uses enviroment file with Devman and Telegram authorization data. The file '.env' must include following data:
- DVMN_API_TOKEN, individual token of Devman API
- TELEGRAM_BOT_TOKEN, Telegram bot token
- TELEGRAM_USER_ID, an ID of a Telegram user who get the notification
- TELEGRAM_USER_NAME, a name of a Telegram user who get the notification
- TELEGRAM_ADMIN_ID, an ID of bot administrator in Telegram to send logging notifications

Python 3 should be already installed. Then use pip3 (or pip) to install dependencies:

```bash
pip3 install -r requirements.txt
```

# How to launch
The Example of launch in Ubuntu is:

```bash
$ python3 send_notification.py 
```

It is better to launch the script on a remote server, [Heroku](https://devcenter.heroku.com/articles/how-heroku-works), for example. It provides that it will work around the clock. A "Procfile" is need to launch correctly on Heroku.

# Project Goals

The code is written for educational purposes on online-course for web-developers dvmn.org, module [Chat Bots with Python](https://dvmn.org/modules/chat-bots/lesson/devman-bot/#review-tabs).

