import telebot
from telebot import types

bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def markup (message):
    markup = types.ReplyKeyboardMarkup ()
    btn1 = types.KeyboardButton('проверка1')
    btn2 = types.KeyboardButton('проверка2')
    btn3 = types.KeyboardButton('проверка3')
    markup.row(btn1,btn2,btn3)
    markup.row(btn1,btn2,btn3)
    file = open('./cyberforum_logo.png', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    #bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)
   
def on_click (message):
    if message.text.lower() == 'проверка1':
        bot.send_message(message.chat.id, 'проверка1 пройдена!')
    elif message.text == 'проверка2':
        bot.send_message(message.chat.id, 'проверка2 пройдена!')

bot.polling(non_stop=True)