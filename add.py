import telebot
import pymysql
from telebot import types
import random

def theme(message):
    global theme = message.text

