from email import message
import telebot
import logging

logger = telebot.logger
bot = telebot.TeleBot('5368398704:AAHzpAZ05uUsZARnCi5AWQEKbpdK6gkIF6o')
#telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['start'])
def start(message):
    if(message.chat.type == 'private'):
        bot.send_message(message.chat.id, 'hi')

bot.infinity_polling(10000)