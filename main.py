import telebot
from telebot import types

bot = telebot.TeleBot('')
custom_message_data = {}
target_chat_id = 00000000

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Отправить заявку")
    item2 = types.KeyboardButton("Консультация")
    item3 = types.KeyboardButton("Ознакомиться с продукцией")
    item4 = types.KeyboardButton("Завершить чат")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Отправить заявку')
def send_application(message):
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items_1_1 = types.KeyboardButton('Бетон')
    markup_1.add(items_1_1)
    bot.send_message(message.chat.id,'Выберите продукцию', reply_markup=markup_1)
    bot.register_next_step_handler(message, send_application_1)

@bot.message_handler(func=lambda message: message.text == 'Бетон')
def send_application_1(message):
    markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items_1_1 = types.KeyboardButton('М100(В7.5)')
    items_1_2 = types.KeyboardButton('М150(В12.5)')
    items_1_3 = types.KeyboardButton('М200(В15)')
    items_1_4 = types.KeyboardButton('М250(В20)')
    items_1_5 = types.KeyboardButton('М300(В22.5)')
    items_1_6 = types.KeyboardButton('М350(В25)')
    items_1_7 = types.KeyboardButton('М400(В30)')
    items_1_8 = types.KeyboardButton('М500(В35)')
    markup_2.add(items_1_1, items_1_2, items_1_3, items_1_4, items_1_5, items_1_6, items_1_7, items_1_8)
    bot.send_message(message.chat.id,'Выберите продукцию', reply_markup=markup_2)
    bot.register_next_step_handler(message, send_application_2)

@bot.message_handler(func=lambda message: message.text == "Консультация")
def consult(message):
    bot.send_message(message.chat.id, "Оставьте свой номер, и мы Вам обязательно позвоним")
    bot.register_next_step_handler(message, consult_phone)

def consult_phone(message):
    bot.send_message(target_chat_id, "Необходима консультация") 
    bot.send_message(target_chat_id, message.text)
    bot.send_message(message.chat.id, "Напишите что-нибудь, чтобы вернуться в начало")
    bot.register_next_step_handler(message, start)

@bot.message_handler(func=lambda message: message.text == "Ознакомиться с продукцией")
def met(message):
    markup_5 = types.InlineKeyboardMarkup()
    items_1_1_1_5 = types.InlineKeyboardButton('Перейти на сайт', url='https://abk-beton.kz/ru')
    markup_5.add(items_1_1_1_5)
    bot.send_message(message.chat.id,'Перейти на сайт компании', reply_markup=markup_5)
    bot.register_next_step_handler(message, start)

@bot.message_handler(func=lambda message: message.text == "Завершить чат")
def end(message):
    bot.send_message(message.chat.id, "До свидания! Будьте здоровы!")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_application_2(message):
    request_text = "Напишите сообщение по следующей форме  "\
                    "1. Кайрат Серик Берикович  " \
                    "2. +7 777 777 77 77  " \
                    "3. 18 кубов  "\
                    "4. 22 сентября 2023  " \
                    "5. 10 часов утра" 
    
    bot.send_message(message.chat.id, '1. Напишите Ваше ФИО')
    bot.send_message(message.chat.id, '2. Напишите Ваш номер телефона')
    bot.send_message(message.chat.id, '3. Сколько кубов Вам необходимо?')
    bot.send_message(message.chat.id, '4. Напишите дату доставки')
    bot.send_message(message.chat.id, '5. Напишите время доставки')
    bot.send_message(message.chat.id, request_text)
    bot.register_next_step_handler(message, request)

def request(message):
    markup_6 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items_1_1_4 = types.KeyboardButton('Подтвердить эту заявку и отправить менеджерам')
    items_1_1_6 = types.KeyboardButton('Удалить заявку')
    items_1_1_5 = types.KeyboardButton('Редактировать заявку')
    markup_6.add(items_1_1_4, items_1_1_5, items_1_1_6)
    bot.send_message(message.chat.id, 'Ваш заказ указан верно?')
    bot.send_message(message.chat.id,'Выберите действие', reply_markup=markup_6)
    global custom_message_data
    custom_message_data[message.chat.id] = {
        'user_data': message.text,
        'confirmed': False
    }
    bot.register_next_step_handler(message, all_datas)

@bot.message_handler(func=lambda message: message.text == "Подтвердить эту заявку и отправить менеджерам")
def all_datas(message):
    user_id = message.chat.id
    if user_id in custom_message_data:
        if custom_message_data[user_id]['confirmed']:
            bot.send_message(user_id, "Заявка уже была подтверждена и отправлена менеджерам.")
        else:
            bot.send_message(user_id, "Спасибо за Вашу заявку!")
            bot.send_message(target_chat_id, "Поступила новая заявка!")
            bot.send_message(target_chat_id, custom_message_data[user_id]['user_data'])
            custom_message_data[user_id]['confirmed'] = True
    else:
        bot.send_message(user_id, "Заявка не найдена.")
    start(message)

@bot.message_handler(func=lambda message: message.text == "Удалить заявку")
def delete_message(message):
    user_id = message.chat.id
    if user_id in custom_message_data:
        del custom_message_data[user_id]
        bot.send_message(user_id, "Ваша заявка удалена.")
    else:
        bot.send_message(user_id, "Заявка не найдена.")
    start(message)

@bot.message_handler(func=lambda message: message.text == "Редактировать заявку")
def edit_message(message):
    user_id = message.chat.id
    if user_id in custom_message_data:
        bot.send_message(user_id, "Редактирование заявки...")
        bot.send_message(user_id, "Введите новые данные:")
        bot.register_next_step_handler(message, update_request)
    else:
        bot.send_message(user_id, "Заявка не найдена.")
        start(message)

def update_request(message):
    user_id = message.chat.id
    if user_id in custom_message_data:
        custom_message_data[user_id]['user_data'] = message.text
        bot.send_message(user_id, "Данные обновлены.")
    else:
        bot.send_message(user_id, "Заявка не найдена.")
    start(message)

bot.polling(none_stop=True)
