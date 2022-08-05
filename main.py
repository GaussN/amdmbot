from ctypes import sizeof
import config
import telebot
from loguru import logger
from typing import List

logger.add('logs/bot_logs.log', format='{time} {level} {message}', level='DEBUG', rotation='10 KB', compression='zip')


bot = telebot.TeleBot(config.BOT_TOKEN)


import sys
sys.path.append('./amdmapi')


@bot.message_handler(commands=['start'])
def start(message):
    logger.debug(f'new user = {message.chat.id}')
    bot.send_message(message.chat.id, 'приветсвтие')


@bot.message_handler(commands=['get_chords'])
def get_chords(message):
    logger.debug(f'user = {message.chat.id} requested achords')
    
    from amdmapi.composition import Composition
    from amdmapi.find_composition import find_conposition
    
    compositions = find_conposition('Гражданская оборона')
    if compositions is not None and len(compositions) != 0:
        markup = telebot.types.InlineKeyboardMarkup()
        
        for composition in compositions:
            #https://amdm.ru/akkordi/
            #24 - одинакова часть для всех ссылок  
            markup = markup.add(telebot.types.InlineKeyboardButton(text=f'{composition.artist} {composition.title}', callback_data=composition.link[24:]))
        bot.send_message(message.chat.id, 'получай', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'не могу найти')
    


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    answer = call.data

    bot.send_message(call.message.chat.id, answer)


bot.infinity_polling()