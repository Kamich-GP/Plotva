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
#Кнопки для вывода товаров
def main_menu_buttons(products_from_db):
    #Создаем пространство для кнопок
    kb = types.InlineKeyboardMarkup(row_width=2)
    #Создаем несгораемые кнопки
    cart = types.InlineKeyboardButton(text='Корзина', callback_data='cart')
    #Создаем кнопки с продуктами
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}',
                                               callback_data=f'{i[0]}')
                    for i in products_from_db]
    #Добавляем кнопки в пространство
    kb.row(cart)
    kb.add(*all_products)

    return kb
#Функция для скрытия кнопок
def remove():
    types.ReplyKeyboardRemove()



