import logging
import aiohttp
import asyncio
from reader import imap_poll
from aiogram import Bot, Dispatcher, executor, types
from reader import proxy_url, proxy_login, proxy_password
from reader import api_token, last_messages_count


proxy_auth = aiohttp.BasicAuth(login=proxy_login, password=proxy_password)
bot = Bot(token=api_token, proxy=proxy_url, proxy_auth=proxy_auth)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello, I am nifti task notifier")


@dp.message_handler(commands=['tasks'])
async def send_message(message: types.Message):
    messages = imap_poll()
    for msg in messages:
        print(msg.content)
        await message.reply(msg.content)
        await asyncio.sleep(0.5)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
