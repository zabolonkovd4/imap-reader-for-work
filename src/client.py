import logging
from aiogram import Bot, Dispatcher, executor, types
import aiohttp
from reader import imap_poll, RepeatedTimer

API_TOKEN = '6336392389:AAHD_IHMcHMolY-gCJ45G9mA14g3JLmL-Nk'
#API_TOKEN = 'TOKEN'

PROXY_URL = "http://http-squid.lab14.ptri.dom:8080"
#PROXY_URL = 'http://PROXY_URL'  # Or 'socks5://host:port'

PROXY_AUTH = aiohttp.BasicAuth(login='diz', password='Zabolonkovd4')
#PROXY_AUTH = aiohttp.BasicAuth(login='login', password='password')
bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
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


#@dp.message_handler()
#async def send_message(content: str):
#    await bot.send_message(message.from_user.id, content)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    #rt = RepeatedTimer(5, imap_poll)
    #rt.start()
    executor.start_polling(dp, skip_updates=True)
