import logging

import telebot
from local_secrets import API_TOKEN

logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s',
                    level=logging.INFO)

bot = telebot.TeleBot(token=API_TOKEN)


def received_tweets_from_api(tweets) -> bool:
    logging.info(tweets)

    try:
        for tweet in tweets:
            bot.send_message(chat_id='@test_channel_twitter_parser',
                             text=tweet.text)
    except Exception as error:
        logging.error(f'An error occurred during sending tweets in tg // '
                      f'{error.args}')
        return False
    else:
        return True
