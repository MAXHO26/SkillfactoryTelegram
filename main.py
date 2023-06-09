import telebot
from conf import keys, TOKEN
from utils import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(message.chat.id, f"Проект для Skillfactory!"),
    bot.reply_to(message, "Чтобы начать работу введите через пробел команду в следующем формате: \
    \n<имя валюты цену которой хотите узнать> \
    <имя валюты в которую конвертируем> \
    <количество валюты>\
    \n Чтобы увидеть список всех доступных валют введите:\
    \n /values"
                )


@bot.message_handler(commands=["values"])
def values(message):
    k = []
    for i in keys.keys():
        k.append(i)
    bot.reply_to(message, 'Доступные валюты\n' + "\n".join(k))


@bot.message_handler(content_types=["text"])
def text(message):
    try:
        v = message.text.split()
        if len(v) > 3:
            raise APIException('Слишком много параметров, повторите команду')
        if len(v) < 3:
            raise APIException('Параметров недостаточно, повторите команду')
        quote, base, amount = v
        te = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя: \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду, повторите команду \n{e}")
    else:
        bot.send_message(message.chat.id, te)


bot.polling(none_stop=True)
