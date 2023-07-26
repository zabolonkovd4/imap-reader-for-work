from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


request_btn = KeyboardButton('/tasks')
request_msgs_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(request_btn)
clear_btn = KeyboardButton('/clear')
clear_chat_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(clear_btn)
