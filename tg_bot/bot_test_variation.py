import asyncio
import logging
from datetime import time
# from main import get_tweets
from aiogram import Bot, Dispatcher, executor, types
import telebot



# Configure logging
from local_secrets import API_TOKEN

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(token=API_TOKEN)
# Initialize bot and dispatcher
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
# updater = Updater(API_TOKEN)
#
# @dp.message_handler(commands=['start', 'help'])
# async def send_welcome(message: types.Message):
#     """
#     This handler will be called when user sends `/start` or `/help` command
#     """
#     await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
#
#
# # @dp.message_handler()
# async def send_new_posts(tweets):
#     # for item in items:
#     #     if item['id'] <= last_id:
#     #         break
#     #     link = '{!s}{!s}'.format(BASE_POST_URL, item['id'])
#     # await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
#     # tweets = get_tweets(5)
#     for tweet in tweets:
#         await bot.send_message(chat_id='@test_channel_twitter_parser', text=tweet)
#     #     # Спим секунду, чтобы избежать разного рода ошибок и ограничений (на всякий случай!)
#
#     # return
#
#
# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#
#     await message.answer(message.text)


def received_tweets_from_api(tweets):
    print(tweets)
    # executor.start_polling(dp, skip_updates=True)
    # send_new_posts(tweets)
    for tweet in tweets:
        # print(tweet.text)
        bot.send_message(chat_id='@test_channel_twitter_parser',
                                           text=tweet.text)
    # executor.start(dp, send_new_posts())

    # asyncio.run(send_new_posts('hi'))
