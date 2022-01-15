import telebot

bot = telebot.TeleBot("5005216647:AAHeTj3pMtbKUz8E_N63YYRNEMfs9X0FY5c", parse_mode=None)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Добрый день!")

bot.infinity_polling()