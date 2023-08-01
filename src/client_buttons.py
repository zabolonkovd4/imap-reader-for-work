from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


request_btn = KeyboardButton('/tasks')
imap_btn = KeyboardButton('/settings')
yes_btn = KeyboardButton('Yes')
no_btn = KeyboardButton('No')
rkm = ReplyKeyboardMarkup(resize_keyboard=True).add(request_btn).add(imap_btn)
rkm_yes_no = ReplyKeyboardMarkup(resize_keyboard=True).add(yes_btn).add(no_btn)
