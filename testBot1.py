import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('')
remove = telebot.types.ReplyKeyboardRemove()

conn = sqlite3.connect('DB_Users.sqlite3')
cur = conn.cursor()
cur.execute('''
 CREATE TABLE IF NOT EXISTS users (id integer primary key AUTOINCREMENT NOT NULL, id_telegram integer, name varchar(50), type integer, phonenumber integer)
 ''')
conn.commit()
cur.close()
conn.close()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('Да')
    btn2 = types.KeyboardButton('Нет')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, "Я вас не узнаю. Желаете пройти процесс авторизации?", reply_markup = markup)

@bot.message_handler(content_types=['text'])
def on_click(message):
    global remove
    if message.text == 'Да':
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, "Для авторизации необходим ваш номер, чтобы предоставить нажмите кнопку ниже", reply_markup=keyboard)
        bot.register_next_step_handler (message, contact_ph)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, "До свидания!", reply_markup=remove)
def contact_ph(message):
    global remove
    if message.content_type == 'contact':
        bot.send_message(message.chat.id, "Вы успешно отправили свой номер", reply_markup = remove)
        phonenumber = str(message.contact.phone_number)
        id_telegram = str(message.from_user.id)
        conn = sqlite3.connect('DB_Users.sqlite3')
        cur = conn.cursor()
        cur.execute("INSERT INTO users(id_telegram, phonenumber) VALUES ('%s', '%s')" % (id_telegram, phonenumber))
        conn.commit()
        cur.close()
        conn.close()
    else:
        message == bot.send_message(message.chat.id, "Необходимо поделиться вашим контактом (нажмите кнопку ниже)")
        bot.register_next_step_handler(message, contact_ph)


bot.polling(non_stop=True)

        #conn = sqlite3.connect('DB_Users.sqlite3')
        #cur = conn.cursor()
        #cur.execute('''
                    #CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, id_telegram integer, name varchar(50), type integer)
                    #''')
        #conn.commit()
        #cur.close()
        #conn.close()

  #cur.execute("INSERT INTO users(id_telegram, name, phonenamber) VALUES ('%s', '%s')" % (id_telegram, name))
        #conn.commit()
        #cur.close()
        #conn.close()

        #№id_telegram = types.InlineKeyboardButton(message.from_user.id)
        #name = types.InlineKeyboardButton(message.from_user.first_name)