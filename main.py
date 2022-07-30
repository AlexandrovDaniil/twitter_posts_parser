import datetime

from tg_bot.bot_test_variation import received_tweets_from_api
from twitter_posts_parser.db import repositories
from db.settings import SessionLocal
from local_secrets import (
    api_key,
    api_secrets,
    access_token,
    access_secret,
    bearer_token
)

import tweepy

client = tweepy.Client(bearer_token)
user = client.get_user(username='ManagingBarca')


def get_tweets(count: int):
    time_end = datetime.datetime.utcnow()
    # time_end = datetime.datetime(2022, 7, 3, 0, 0)
    time_start = datetime.datetime(2022, 7, 1, 0, 0)
    # res = client.get_users_tweets(id=user.data.id, start_time=time_start,
    #                               end_time=time_end, max_results=count)
    res = client.get_users_tweets(id=user.data.id, max_results=count)
    print(res.meta['result_count'])
    print(res)
    tweets = []

    last_load_id = get_last_row().tweet_id
    status = True
    update_last_load(res.data[0].id, str(datetime.datetime.utcnow()))
    for tweet in res.data:
        if tweet.id == last_load_id:
            status = False
        if status:
            tweets.append(tweet)

    send_tweets_to_tg(tweets)

    return tweets


def get_last_row():
    session_local = SessionLocal()
    d = repositories.LastLoadRepo(session_maker=session_local)
    return d.get_last_load()


def update_last_load(tweet_id: int, time_of_update: str):
    session_local = SessionLocal()
    d = repositories.LastLoadRepo(session_maker=session_local)
    d.update_information(tweet_id, time_of_update)


def send_tweets_to_tg(tweets):
    if not tweets:
        print('tweets list is empty')
        return
    print('ready to send to post tweets in tg')
    for tweet in tweets:
        tweet.text = tweet.text.replace('&amp;', '&')
    received_tweets_from_api(tweets)


get_tweets(10)
# for i in get_tweets(10):
#     print(i)
