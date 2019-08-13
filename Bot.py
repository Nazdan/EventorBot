import telebot
import pymysql
from telebot import types
from time import timezone
import apiai
import json
import datetime


token = '721442351:AAHTxBWlgwvtz3tmDhPwcRkKeXo5WxC6lgk'
count = 10
the = ''
my_town = ''
my_address = ''
what = True

db = pymysql.connect(host='sql7.freemysqlhosting.net', user='sql7301609', passwd='8swRXjLsGN', db='sql7301609', charset='utf8mb4')
cursor = db.cursor()

hide = types.ReplyKeyboardRemove()  # Спрятанная клавиатура

choice1 = types.ReplyKeyboardMarkup()
choice1.row(types.KeyboardButton('Посмотреть'), types.KeyboardButton('Добавить'))

town_markup = types.ReplyKeyboardMarkup()
town_markup.row(types.KeyboardButton('Москва'), types.KeyboardButton('Казань'))

meet = types.KeyboardButton('Встреча')
sport = types.KeyboardButton('Спорт')
music = types.KeyboardButton('Музыка')
other = types.KeyboardButton('Другое')
abort = types.KeyboardButton('Отмена')

theme_markup = types.ReplyKeyboardMarkup()
theme_markup_add = types.ReplyKeyboardMarkup()

theme_markup.row(meet, sport, music)
theme_markup.row(other, types.KeyboardButton('Всё'))

theme_markup_add.row(meet, sport, music)
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
    global what
    if message.text == 'Посмотреть':  # Просмотр ивентов
        what = True
        bot.send_message(message.chat.id, 'Выберите город', reply_markup=town_markup)
        bot.register_next_step_handler(message, town_)
    else:
        what = False
        bot.send_message(message.chat.id, 'Выберите город', reply_markup=town_markup)
        bot.register_next_step_handler(message, town_)


def town_(message):
    global my_town
    my_town = message.text
    if what:
        bot.send_message(message.chat.id, 'Выберите тему', reply_markup=theme_markup)
        bot.register_next_step_handler(message, look_)
    else:
        bot.send_message(message.chat.id, 'Выберите тему', reply_markup=theme_markup_add)
        bot.register_next_step_handler(message, theme)


def look_(message):  # Просмотр ивентов
    snd = ''
    theme4sort = message.text
    if theme4sort == 'Всё':
        command = "SELECT * FROM `events_event` WHERE event_city = '{}'".format(my_town)
    else:
        command = "SELECT * FROM `events_event` WHERE event_theme = '{}' AND event_city = '{}'".format(theme4sort, my_town)
    cursor.execute(command)
    data = cursor.fetchall()
    for event in data:
        snd += event[2] + " " + str(event[3]) + '\n' + event[5] + '\n' + event[7] + '\n' * 2
    bot.send_message(message.chat.id, snd)
    start(message, False)


def theme(message):
    if message.text == 'Отмена':
        start(message, False)
    else:
        global the
        the = message.text
        bot.send_message(message.chat.id,
                         "Напишите адресс места проведения мероприятия")
        bot.register_next_step_handler(message, create)


def create(message):
    if message.text == 'Отмена':
        start(message, False)
    else:
        global my_address
        my_address = message.text
        bot.send_message(message.chat.id,
                         "Напишите информацию о  вашем событии")
        bot.register_next_step_handler(message, crutch)


def crutch(message):
    if message.text == 'Отмена':
        start(message, False)
    else:
        dialogflow(message, [])


def dialogflow(message, context):
    request = apiai.ApiAI('716c31c2ff3a4fd390b14923be5b68e5').text_request()
    request.lang = 'ru'
    request.session_id = str(message.chat.id)
    request.query = message.text
    request.contexts = context
    response = json.loads(request.getresponse().read().decode('utf-8'))
    print(response)
    try:
        if response['result']['resolvedQuery'] == 'Отмена':
            print(1)
            bot.send_message(message.chat.id, "Что выберешь?", reply_markup=choice1)
            bot.register_next_step_handler(message, choose)
        elif response['result']['contexts'][0]['parameters']['theme'] == '' or \
                response['result']['contexts'][0]['parameters']['date'] == '' or response['result']['contexts'][0]['parameters']['time'] == '':
            bot.send_message(message.chat.id, response['result']['fulfillment']['speech'])
            bot.register_next_step_handler(message, dialogflow, response['result']['contexts'])
            print(2)
        elif response['result']['metadata']['intentName'] == 'create_event':
            print(3)
            bot.send_message(message.chat.id, response['result']['fulfillment']['speech'])
            bot.register_next_step_handler(message, dialogflow, response['result']['contexts'])
        elif response['result']['metadata']['intentName'] == 'yes_event':
            print('oooo')
            # типо записали в БД эти два значения
            bot.send_message(message.chat.id, response['result']['fulfillment']['speech'])
            name = response['result']['contexts'][0]['parameters']['theme']
            date = response['result']['contexts'][0]['parameters']['date']
            time = response['result']['contexts'][0]['parameters']['time']
            print(date, time)
            command = "INSERT INTO `events_event`(`event_owner`, `event_name`, `event_date`, `event_theme`, " \
                      "`event_address`, `event_city`, `event_text`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', " \
                      "'Без описания')".format(message.from_user.id, name, date +  " " + time, the, my_address, my_town)
            cursor.execute(command)
            db.commit()
            bot.send_message(message.chat.id, 'Вы успешно создали мероприятие! Выбирайте что дальше...', reply_markup=choice1)
            bot.register_next_step_handler(message, choose)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, response['result']['fulfillment']['speech'])


bot.polling(none_stop=True)
