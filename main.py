import datetime
import logging
import re
import time
from typing import Optional

import tweepy
from db.entities import TweetInformation
from db.settings import SessionLocal
from local_secrets import (access_secret, access_token, api_key, api_secrets,
                           bearer_token)
from tg_bot.bot_test_variation import received_tweets_from_api

from twitter_posts_parser.db import repositories

client = tweepy.Client(bearer_token)
user = client.get_user(username='ManagingBarca')


logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s',
                    level=logging.INFO)


def get_tweets(count: int):
    res = client.get_users_tweets(id=user.data.id, max_results=count)

    tweets = []

    last_load_id = get_last_row().tweet_id
    status = True

    for tweet in res.data:
        if tweet.id == last_load_id:
            status = False
        if status:
            tweets.append(tweet)

    messages_send = send_tweets_to_tg(tweets)

    if messages_send:
        update_last_load(
            int(res.meta['newest_id']), str(datetime.datetime.utcnow())
        )

    return tweets


def get_last_row() -> Optional[TweetInformation]:
    session_local = SessionLocal()
    d = repositories.LastLoadRepo(session_maker=session_local)
    return d.get_last_load()


def update_last_load(tweet_id: int, time_of_update: str) -> None:
    session_local = SessionLocal()
    d = repositories.LastLoadRepo(session_maker=session_local)
    d.update_information(tweet_id, time_of_update)


def send_tweets_to_tg(tweets) -> Optional[bool]:
    if not tweets:
        logging.warning('tweets list is empty')

        return False

    logging.info('ready to send to post tweets in tg')

    for tweet in tweets:
        tweet.text = tweet.text.replace('&amp;', '&')
        tweet.text = re.sub('[^A-Za-z0-9-/().&@:\' ]+', '', tweet.text)
        tweet.text = tweet.text.replace('@', '\nvia: https://twitter.com/')

    messages_send = received_tweets_from_api(tweets[::-1])

    return messages_send


while True:
    get_tweets(5)
    time.sleep(300)
