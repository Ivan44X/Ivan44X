import telebot
import sqlite3

name = 'None'

bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start (message):
    conn = sqlite3.connect('test1.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar (50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, введи свое имя')
    bot.register_next_step_handler(message, user_name)

def user_name (message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass (message):
    password = message.text.strip()
    conn = sqlite3.connect('test1.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name, pass) VALUES ('%s', '%s')" % (name,password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id,'Пользователь зарегистрирован')

@bot.message_handler(commands=['stp'])
def stp (message):
    bot.send_message(message.chat.id, name)

 
#   bot.send_message(message.chat.id, 'Введите пароль')
#   bot.register_next_step_handler(message, user_pass)

bot.polling(non_stop=True)