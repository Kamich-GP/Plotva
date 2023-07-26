from telebot import types

#Кнопка для отправки номера
def num_button():
    #Создаем пространство для кнопок
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    #Создаем сами кнопки
    num = types.KeyboardButton('Отправить номер', request_contact=True)

    #Добавляем кнопки в пространство
    kb.add(num)
    return kb
#Кнопка для отправки локации
def loc_button():
    # Создаем пространство для кнопок
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Создаем сами кнопки
    loc = types.KeyboardButton('Отправить геопозицию', request_location=True)

    # Добавляем кнопки в пространство
    kb.add(loc)
    return kb
#Функция для скрытия кнопок
def remove():
    types.ReplyKeyboardRemove()



