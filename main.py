import telebot
import tokn
from telebot import types
from sql import SQLite
from parse import Parser

db = SQLite('database.db')
bot = telebot.TeleBot(tokn.Token)


@bot.message_handler(commands=['start'])
def start(message):
    if (not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id)
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Курсы валют Qiwi", callback_data='update')
    markup.add(button)
    bot.send_message(message.chat.id,
                     "Привет😉\nЯ всегда подскажу актуальные курсы валют Qiwi, если, конечно, компьютер моего создателя будет включен!",
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     "Помогаю следить за курсами валют Qiwi\n\n/start - перезапустить бота\n/currency - узнать актуальный курс валют\n/update - обновить курс валют\n/sub - подписаться на рассылку курса валют\n/unsub - отписаться от рассылки\n/contacts - связь с разработчиком")


@bot.message_handler(commands=['update'])
def update(message):
    return currency(message)


@bot.message_handler(commands=['contacts'])
def contacts(message):
    markup = types.InlineKeyboardMarkup()
    item = [
        types.InlineKeyboardButton(text="Telegram", url="https://t.me/UtxIDtXzgix"),
        types.InlineKeyboardButton(text="VK", url="https://vk.com/pharsifal"),
        types.InlineKeyboardButton(text="⏮Назад", callback_data='cancel')
    ]
    markup.add(*item)
    bot.send_message(message.chat.id, "Всем привлет!", reply_markup=markup)


@bot.message_handler(commands=['freemoney'])
def freeMoney(message):
    rickRoll = types.InlineKeyboardMarkup()
    rickItem = [
        types.InlineKeyboardButton(text="Бесплатные деньги тут", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        types.InlineKeyboardButton(text="⏮Назад", callback_data='cancel')
    ]
    rickRoll.add(*rickItem)
    bot.send_message(message.chat.id, "Точно не обман!!", reply_markup=rickRoll)


@bot.message_handler(commands=['sub'])
def subscribe(message):
    if (db.subscription_active(message.from_user.id, False)):
        db.update_subscription(message.from_user.id, True)
        bot.send_message(message.chat.id, "Вы успешно подписались на рассылку!")
    else:
        bot.send_message(message.chat.id, "Вы уже подписаны на рассылку!")


@bot.message_handler(commands=['unsub'])
def unsubscribe(message):
    if (db.subscription_active(message.from_user.id, True)):
        db.update_subscription(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы успешно отписались от рассылки!")
    else:
        bot.send_message(message.chat.id, "Вы не подписаны на рассылку!")


@bot.message_handler(commands=['currency'])
def currency(message):
    global cur
    msg = bot.send_message(message.chat.id, "Обновляю котировки...")
    cur = Parser.result(message.chat.id)
    bot.delete_message(message.chat.id, msg.message_id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = [
        types.InlineKeyboardButton(text="🇰🇿 KZT", callback_data='kzt'),
        types.InlineKeyboardButton(text="🇺🇸 USD", callback_data='usd'),
        types.InlineKeyboardButton(text="🇪🇺 EUR", callback_data='eur'),
        types.InlineKeyboardButton(text="🇨🇳 CNY", callback_data='cny'),
        types.InlineKeyboardButton(text="Обновить котировки 🔄", callback_data='update')
    ]
    markup.add(*item)
    bot.send_message(message.chat.id, "Выберите валюту", reply_markup=markup)


@bot.message_handler(commands=['kzt'])
def kzt(message):
    bot.send_message(message.chat.id, f'🇰🇿 100 KZT\nПокупка: {str(cur[1])} RUB\nПродажа: {str(cur[2])} RUB')


@bot.message_handler(commands=['usd'])
def usd(message):
    bot.send_message(message.chat.id, f'🇺🇸 1 USD\nПокупка: {str(cur[4])} RUB\nПродажа: {str(cur[5])} RUB')


@bot.message_handler(commands=['eur'])
def eur(message):
    bot.send_message(message.chat.id, f'🇪🇺 1 EUR\nПокупка: {str(cur[7])} RUB\nПродажа: {str(cur[8])} RUB')


@bot.message_handler(commands=['cny'])
def cny(message):
    bot.send_message(message.chat.id, f'🇨🇳 1 CNY\nПокупка: {str(cur[10])} RUB\nПродажа: {str(cur[11])} RUB')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == "help":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            return help(call.message)
        elif call.data == "contacts":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            return contacts(call.message)
        elif call.data == "freemoney":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            return freeMoney(call.message)
        elif call.data == "currency":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            return currency(call.message)
        elif call.data == "cancel":
            return help(call.message)
        elif call.data == "update":
            return currency(call.message)
        elif call.data == "kzt":
            return kzt(call.message)
        elif call.data == "usd":
            return usd(call.message)
        elif call.data == "eur":
            return eur(call.message)
        elif call.data == "cny":
            return cny(call.message)


if __name__ == '__main__':
    bot.polling()
