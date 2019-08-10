import telebot
import pymysql
from telebot import types

token = '721442351:AAHTxBWlgwvtz3tmDhPwcRkKeXo5WxC6lgk'
count = 10
the = ''

db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='events', charset='utf8mb4')
cursor = db.cursor()

hide = types.ReplyKeyboardRemove()  # Спрятанная клавиатура
choice1 = types.ReplyKeyboardMarkup()

choice1.row(types.KeyboardButton('Посмотреть'), types.KeyboardButton('Добавить'))

meet = types.KeyboardButton('Встреча')
sport = types.KeyboardButton('Спорт')
other = types.KeyboardButton('Другое')
abort = types.KeyboardButton('Отмена')

theme_markup = types.ReplyKeyboardMarkup()
theme_markup_add = types.ReplyKeyboardMarkup()

theme_markup.row(meet, sport)
theme_markup.row(other, types.KeyboardButton('Всё'))

theme_markup_add.row(meet, sport)
theme_markup_add.row(other, abort)

bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=["start", 'd'])
def start(message, ter=True):
    if ter:  # ter=True, если функция вызывается по окончанию добавления/просмотра ивентов
        bot.send_message(message.chat.id, 'Привет! Что хочешь сделать?', reply_markup=choice1)
    else:
        bot.send_message(message.chat.id, 'Что хочешь сделать?', reply_markup=choice1)
    bot.register_next_step_handler(message, choose)


def choose(message):
    if message.text == 'Посмотреть':  # Просмотр ивентов
        bot.send_message(message.chat.id, 'Выберите тему', reply_markup=theme_markup)
        bot.register_next_step_handler(message, look_)
    else:
        bot.send_message(message.chat.id, 'Выберите тему', reply_markup=theme_markup_add)
        bot.register_next_step_handler(message, theme)


def look_(message):  # Просмотр ивентов
    snd = ''
    theme4sort = message.text
    if theme4sort == 'Всё':
        command = 'SELECT * FROM `all` WHERE 1'
    else:
        command = "SELECT * FROM `all` WHERE theme = '{}'".format(theme4sort)
    cursor.execute(command)
    data = cursor.fetchall()
    for event in data:
        snd += event[2] + " " + event[3] + ' ' + event[4] + '\n' + event[5] + '\n' + event[7] + '\n' * 2
    bot.send_message(message.chat.id, snd)
    start(message, False)


def theme(message):
    if message.text == 'Отмена':
        start(message, False)
    else:
        global the
        the = message.text
        bot.send_message(message.chat.id,
                         "Напишите информацию о  вашем событии по шаблону \n Название \n Дата \n Время "
                         "\n Место проведения \n Описание \n Вместо пустых полей не забывайте ставить "
                         "прочерки(-)")
        bot.register_next_step_handler(message, create)


def create(message):
    if message.text == 'Отмена':
        start(message, False)
    else:
        global count
        l = message.text.split('\n')
        print(l)
        command = "INSERT INTO `all`(`user_id`, `event_id`, `name`, `date`, `time`, `adress`, `theme`, `description`)" \
                  " VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(message.from_user.id, str(count), l[0],
                                                                                   l[1], l[2], l[3], the, l[4])
        cursor.execute(command)
        db.commit()
        count += 1
        bot.send_message(message.chat.id, 'ГОТОВО!')
        start(message, False)


bot.polling(none_stop=True)
