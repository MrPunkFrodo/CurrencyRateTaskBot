import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrensyConverter
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы конвертера введите команду в следующем формате: \n <Валюта, цену которой хотите узнать> \
<Валюта, в которой хотите узнать цену первой валюты> \
<количество первой валюты>\n Чтобы увидеть список доступных валют введите: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')
        if len(value) != 3:
            raise ConvertionException('Введено неверное кол-во параметров')
        quote, base, amount = value
        total_base = CurrensyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'цена {amount} {quote} в {base} это {float(total_base) * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()
