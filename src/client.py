import logging
import aiohttp
import asyncio
import collections
import re
from reader import imap_poll, env
from aiogram import Bot, Dispatcher, executor, types
from client_buttons import rkm, rkm_yes_no


def restart_dispatcher():
    proxy_auth = aiohttp.BasicAuth(login=env.proxy_username, password=env.proxy_password)
    bot = Bot(token=env.api_token, proxy=env.proxy_url, proxy_auth=proxy_auth)
    return Dispatcher(bot)


dp = restart_dispatcher()
logging.basicConfig(level=logging.INFO)


def new_config_param(param_name: str) -> str:
    return f'New config parameter:\n {param_name}'


@dp.message_handler(commands=['start', 's'])
async def send_welcome(message: types.Message):
    await message.reply("Hello, I am nifti task notifier", reply_markup=rkm)


@dp.message_handler(commands=['settings'])
async def send_message(message: types.Message):
    await message.reply('Current imap configuration:\n'
                        f'imap_server: {env.imap_server}\n'
                        f'imap_username: {env.imap_username}\n'
                        f'imap_password: <span class="tg-spoiler">{env.imap_password}</span>\n'
                        f'proxy_url: {env.proxy_url}\n'
                        f'proxy_username: {env.proxy_username}\n'
                        f'proxy_password: <span class="tg-spoiler">{env.proxy_password}</span>\n'
                        f'last_messages_count: {env.last_messages_count}',
                        parse_mode='html',
                        reply_markup=rkm)
    await message.reply('Would you like to change it?', reply_markup=rkm_yes_no)


@dp.message_handler(lambda message: message.text.startswith('imap_server='))
async def imap_server_changing(message: types.Message):
    if env.changing_configuration:
        env.imap_server = message.text.partition("=")[2]
        await message.reply(new_config_param(message.text))
        env.changing_configuration = False
    else:
        await echo(message)


@dp.message_handler(lambda message: message.text.startswith('imap_username='))
async def imap_username_changing(message: types.Message):
    if env.changing_configuration:
        env.imap_username = message.text.partition("=")[2]
        await message.reply(new_config_param(message.text))
        env.changing_configuration = False
    else:
        await echo(message)


@dp.message_handler(lambda message: message.text.startswith('imap_password='))
async def imap_password_changing(message: types.Message):
    if env.changing_configuration:
        env.imap_password = message.text.partition("=")[2]
        await message.reply(new_config_param(message.text))
        env.changing_configuration = False
    else:
        await echo(message)


@dp.message_handler(lambda message: message.text.startswith('proxy_url='))
async def proxy_url_changing(message: types.Message):
    if env.changing_configuration:
        env.proxy_url = message.text.partition("=")[2]
        await message.reply(new_config_param(message.text))
        global dp
        dp = restart_dispatcher()
        env.changing_configuration = False
    else:
        await echo(message)


@dp.message_handler(lambda message: message.text.startswith('proxy_username='))
async def proxy_username_changing(message: types.Message):
    if env.changing_configuration:
        env.proxy_username = message.text.partition("=")[2]
        await message.reply(new_config_param(message.text))
        global dp
        dp = restart_dispatcher()
        env.changing_configuration = False
    else:
        await echo(message)


@dp.message_handler(lambda message: message.text.startswith('proxy_password='))
async def proxy_password_changing(message: types.Message):
    if env.changing_configuration:
        env.proxy_password = message.text.partition("=")[2]
        await message.reply(new_config_param(message.text))
        global dp
        dp = restart_dispatcher()
        env.changing_configuration = False
    else:
        await echo(message)


@dp.message_handler(lambda message: message.text.startswith('last_messages_count='))
async def last_messages_count_changing(message: types.Message):
    if env.changing_configuration:
        env.last_messages_count = int(re.findall("\d+", message.text)[0])
        await message.reply(new_config_param(message.text))
        env.changing_configuration = False
    else:
        await echo(message)


@dp.message_handler(lambda message: message.text == 'Yes')
async def send_on_yes(message: types.Message):
    env.changing_configuration = True
    await message.reply('So, carefully type configuration in format bellow:\n'
                        'imap_server=<server_url>', reply_markup=rkm)


@dp.message_handler(lambda message: message.text == 'No')
async def send_on_no(message: types.Message):
    await message.reply('Okay!', reply_markup=rkm)


@dp.message_handler(commands=['tasks', 't'])
async def send_message(message: types.Message):
    messages = imap_poll()
    # ordering messages for telegram chat
    messages = collections.OrderedDict(reversed(list(messages.items())))
    for msg in messages:
        print(msg.content)
        await message.reply(msg.content)
        await asyncio.sleep(0.5)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Type /tasks or push the request button from keyboard', reply_markup=rkm)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
