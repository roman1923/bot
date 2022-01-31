import telebot
from extensions import Convertor, APIException
from config import exchanges, TOKEN
import traceback

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '\n<Имя валюты цену которой вы хотите узнать>\ \<В какую перевести>\ \<Количество переводимой валюты>\ \nСписок всех валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Имя валюты цену которой вы хотите узнать:'
    bot.reply_to(message, text)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = 'Выберите валюту, в которую конвертировать:'
    bot.reply_to(message, text)
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = 'Выберите количество валюты:'
    bot.reply_to(message, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        answer = Convertor.get_price(base, quote, amount) 
    except APIException as e:
        bot.send_message(message.chat.id, f"Fall convertion: \n{e}")
    else:
        text = f"Цена {amount} {base} в {quote} : {answer}"
        bot.reply_to(message,text)
        bot.register_next_step_handler(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        
        answer =  Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message,answer)

bot.polling()