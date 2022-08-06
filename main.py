import sys
import config
import telebot
from loguru import logger
from typing import List


logger.add('logs/bot_logs.log', format='{time} | {level} | {message}', level='INFO', rotation='10 KB', compression='zip')

bot = telebot.TeleBot(config.BOT_TOKEN)

sys.path.append('./amdmapi')
from amdmapi.composition import Composition
from amdmapi.find_composition import find_conposition
from amdmapi.get_composition import get_composition


logger.info('Бот запущен')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    try:
        logger.info(f'new user: {message.chat.id}')
        bot.send_message(
            message.chat.id, 
            'Этот бот поможет тебе найти аккорды к песне. Для использования введи /get_сhords <Название песни>'
        )        
    except:
        pass

#поиск композиций 
@bot.message_handler(commands=['get_chords'])
def get_chords(message):
    argv = message.text.split()
    if len(argv) == 1:
        bot.send_message(message.chat.id, 'введите название песни вместе с командой')
        return
    
    find = " ".join(argv[1:])
    logger.info(f'user({message.chat.id}) requested achords({find})')
    
    compositions = find_conposition(find)
    if compositions is not None and len(compositions) != 0:
        markup = telebot.types.InlineKeyboardMarkup()
        
        #callback max - 64
        
        for composition in compositions:
            link = composition.link[24:]
            #иначе ошибка будет 
            if len(link) <= 64:
                markup.add(
                    telebot.types.InlineKeyboardButton(
                        text=f'{composition.artist} {composition.title}', 
                        callback_data=link
                    )
                )
               
        bot.send_message(message.chat.id, 'Выберите', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Ничего не могу найти')
    


#отправка аккордов
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        answer = get_composition(link=f'https://amdm.ru/akkordi/{call.data}') 
        bot.send_message(call.message.chat.id, answer)        
        logger.info(f'user({call.message.chat.id}) got chords')
    except:
        bot.send_message(call.message.chat.id, 'Ошибка при отправке аккордов') 


bot.infinity_polling()
