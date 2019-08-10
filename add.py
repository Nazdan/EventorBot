from Bot import db, cursor, bot, start
import pymysql
from telebot import types
import random

the = ''
cnt = 1


def theme(message):
    global the
    the = message.text
    bot.send_message(message.chat.id, "Напишите информацию о  вашем событии по шаблону \n Название \n Дата \n Время "
                                      "\n Место \n проведения \n Описание")
    bot.register_next_step_handler(message, create)


def create(message):
    l = [message.text.split('\n')]
    command = "INSERT INTO `all`(`user_id`, `event_id`, `name`, `date`, `time`, `adress`, `theme`, `description`)" \
              " VALUES ({}, {}, {}, {}, {}, {}, {}, {})".format(message.from_user.id, cnt, l[0], l[1], l[2], l[3], the, l[4])
    cursor.execute(command)
    db.commit()
    bot.send_message(message.chat.id, 'ГОТОВО!')
    bot.register_next_step_handler(message, start(False))
