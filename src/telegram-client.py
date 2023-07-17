import logging

from aiogram import Bot, Dispatcher, executor, types
import aiohttp

API_TOKEN = 'TOKEN'
PROXY_URL = 'http://PROXY_URL'  # Or 'socks5://host:port'
PROXY_AUTH = aiohttp.BasicAuth(login='login', password='password')

bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello, I am nifti task notifier")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
