import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('5222512184:AAEc2sILA6AqhvwKv0aYZIROZQ5cvfJfurc')

def sqlcommand(command):
    connection = sqlite3.connect("itstep_DB.sl3", 5)
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()

    if command.count('SELECT')>0:
        return cur.fetchall()
    connection.close()



@bot.message_handler(commands = ['start'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Хело', url='https://github.com/VadymKuntso1')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Перейти на гітхаб", reply_markup=markup)


@bot.message_handler(commands = ['list'])
def list(message):
    command = 'SELECT * from Traktors'
    res = sqlcommand(command)
    for post in res:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Купити'+str(post[1]), callback_data='buy'+str(post[0]))
        markup.add(button1)

        img = open('img\\{0}'.format(post[2]), 'rb')
        bot.send_photo(message.from_user.id, img)
        text ='''{0}\nЦіна{1}'''.format(post[1], post[3])
        bot.send_message(message.from_user.id, text,reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Хело':
        bot.send_message(message.from_user.id, 'Привіт'+str(message.from_user.id))
    if message.text == 'create':
        print('create')

        command = ('''INSERT INTO Traktors VALUES(0,"first","first.jpg",12000)
''')
        result = sqlcommand(command)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if str(call.data).startswith('buy'):

        sent = bot.send_message(call.from_user.id, 'Input you contacts')
        bot.register_next_step_handler(sent, confirm)

def confirm(message):
    text = '''You contacts: {0}
Thanks, wait for our manager
    '''.format(message.text)
    bot.send_message(message.from_user.id, text)


bot.polling(none_stop=True, interval=0)
