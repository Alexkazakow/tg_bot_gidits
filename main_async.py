import random
import asyncio
import sqlite3
import numpy as np 
from telebot.async_telebot import AsyncTeleBot
from telebot import types

bot = AsyncTeleBot('TOKEN')
digit, number = 0, 0
dct = {'0': '0⃣', '1': '1⃣', '2': '2⃣', '3': '3⃣', '4':'4⃣', '5':'5⃣', '6':'6⃣', '7':'7⃣', '8':'8⃣', '9':'9⃣'}

conn = sqlite3.connect('rating.db', check_same_thread=False)
cursor = conn.cursor()

def add_decision(username: str, digit: int, number: int, decision: str, cnt_number: int, rating: int):
    cursor.execute('INSERT INTO rating (username, digit, number, decision, cnt_number, rating) VALUES (?, ?, ?, ?, ?, ?)', (username, digit, number, decision, cnt_number, rating))
    conn.commit()

def select_my_rating(username):
    cursor.execute('SELECT CASE WHEN EXISTS(SELECT * FROM rating WHERE username = ?) = 0 THEN 0 ELSE SUM(rating) END FROM rating WHERE username = ?', (username, username))
    return cursor.fetchall()[0][0]

def all_record(digit, number):
    cursor.execute('SELECT CASE WHEN EXISTS(SELECT * FROM rating WHERE digit = ? and number = ?) = 0 THEN 0 ELSE MIN(cnt_number) END FROM rating WHERE digit = ? and number = ?', (digit, number, digit, number))
    return cursor.fetchall()[0][0]

@bot.message_handler(commands=['start'])
async def game(message):
    global digit, number
    digit = random.randint(1,9)
    number = random.randint(10,20)
    # str_digit = dct[str(digit)]
    # str_number = ''.join([dct[i] for i in list(str(number))])
    await bot.send_message(message.from_user.id, f'Составьте число {number} из цифры {digit}')


@bot.message_handler(commands=['help'])
async def help(message):
    await bot.send_message(message.from_user.id, f'ЗАДАЧА: \nСоставить из минимального количества простых цифр сложное число \n \nПРИМЕР:\nСоставьте число 120 из цифры 9 \n \nРЕШЕНИЕ: 9 + 999/9 = 120 \n \nРАЗРЕШЕНО ИСПОЛЬЗОВАТЬ: \n + сложение    – вычитание \n* умножение   / деление \n() скобки          ^ степень \n ! факториал')


@bot.message_handler(commands=['rating'])
async def rating(message):
    my_rating = select_my_rating(message.from_user.username) 
    await bot.send_message(message.from_user.id, f'@{message.from_user.username}: {my_rating}')


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    global digit, number
    with open('logs.txt', 'a') as the_file:
        the_file.write(f'{message.text}\n')
    try:
        res = eval(message.text.replace('^', '**'))
        print(res)
        lst = list(message.text)
    except:
        res = 'ошибка'
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.from_user.id, f'{message.text} = {res}')
    if res % 1 == 0 and res == number and sum([x.isdigit() for x in lst]) == lst.count(str(digit)):
        add_decision(username=message.from_user.username, digit=digit, number=number, decision=message.text, cnt_number=lst.count(str(digit)), rating=(1/np.log(lst.count(str(digit)))))
        my_rating = select_my_rating(message.from_user.username)
        record = all_record(digit, number)
        await bot.send_message(message.from_user.id, f'Так держать 👍 \nВы использовали: {lst.count(str(digit))} цифр \nРекорд: {record} цифр\nВаш рейтинг: {round(my_rating, 2)}') #\nЗаработали {round(1/np.log(lst.count(str(digit))), 2)} очков 
        


asyncio.run(bot.polling())
