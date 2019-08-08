import telebot
import time
from telebot import types

token = ""

hide = types.ReplyKeyboardRemove() # Спрятанная клавиатура
choice1 = types.ReplyKeyboardMarkup()
choice1.row(types.KeyboardButton('Посмотреть'), types.KeyboardButton('Добавить'))

bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=["start"])
def start(message, ter=True):
    if ter: #ter=True, если функция вызывается по окончанию добавления/просмотра ивентов
        bot.send_message(message.chat.id, 'Привет! Что хочешь сделать?', reply_markup=choice1)
    else:
        bot.send_message(message.chat.id, 'Что хочешь сделать?', reply_markup=choice1)
    bot.register_next_step_handler(message, choose)


def choose(message):
    if message.text == 'Посмотреть': #Просмотр ивентов
        count = 1
        list = []
        with open('data.txt') as file:
            for i in file:
                list.append(i)
            print(list)
            for i in list:
                bot.send_message(message.chat.id, str(count) + ') ' + i + '\n')
                count += 1
        start(message, False)
    else:
        bot.send_message(message.chat.id, 'Что хочешь добавить?')
        bot.register_next_step_handler(message, add_)


def add_(message): #Добавление ивентов
    with open('data.txt', 'a') as file:
        curtime = time.ctime()
        curtime = curtime[3:]
        file.write(curtime + ': ' + message.text + '\n')
    bot.send_message(message.chat.id, 'Готово!')
    start(message, False)


bot.polling(none_stop=True)
