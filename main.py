import telebot
import bottoken

bot = telebot.TeleBot(bottoken.TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Добрый день!")


bot.infinity_polling()
