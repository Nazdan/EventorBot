import telebot
import pymysql
from telebot import types
import random


token = ''
bor = telebot.TeleBot(token=token)

def theme(message, count):
    global count
    global theme = message.text
    bot.send_message(message.chat.id, "Напишите информацию о  вашем событии по шаблону \n Название \n Дата \n Время \n Место \n проведения \n Описание")
    bot.register_next_step_handler(message, create)


def create(message):
    count += 1
    l = [message.text.split('\n')]
    command = "INSERT INTO `all`(`user_id`, `event_id`, `name`, `date`, `time`, `adress`, `theme`, `description`)" \
              " VALUES ({},{},{},{},{},{},{},{})".format(message.from_user.id, count, l[0], l[1], l[2], l[3], theme, l[4])
    cursor.execute(command)
    db.commit()
    bot.send_message(message.chat.id, 'ГОТОВО!')