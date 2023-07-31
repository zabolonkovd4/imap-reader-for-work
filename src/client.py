import logging
import aiohttp
import asyncio
import collections
from reader import imap_poll
from aiogram import Bot, Dispatcher, executor, types
from reader import proxy_url, proxy_login, proxy_password
from reader import api_token
from client_buttons import request_msgs_kb, clear_chat_btn


proxy_auth = aiohttp.BasicAuth(login=proxy_login, password=proxy_password)
bot = Bot(token=api_token, proxy=proxy_url, proxy_auth=proxy_auth)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start', 's'])
async def send_welcome(message: types.Message):
    await message.reply("Hello, I am nifti task notifier", reply_markup=request_msgs_kb)


@dp.message_handler(commands=['clear', 'c'])
async def clear_chat():
    pass


@dp.message_handler(commands=['tasks', 't'])
async def send_message(message: types.Message):
    messages = imap_poll()
    # ordering meesage for telegram chat
    messages = collections.OrderedDict(reversed(list(messages.items())))
    for msg in messages:
        print(msg.content)
        await message.reply(msg.content)
        await asyncio.sleep(0.5)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Type /tasks or push the request button from keyboard', reply_markup=request_msgs_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
