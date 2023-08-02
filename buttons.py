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
    kb = types.InlineKeyboardMarkup(row_width=1)
    #Создаем несгораемые кнопки
    cart = types.InlineKeyboardButton(text='Корзина', callback_data='cart')
    #Создаем кнопки с продуктами
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}',
                                               callback_data=f'{i[0]}')
                    for i in products_from_db]
    #Добавляем кнопки в пространство
    kb.add(*all_products)
    kb.row(cart)

    return kb

#Кнопки для выбора количества товара
def choose_product_count(amount=1, plus_or_minus=''):
    #Создаем пространство для кнопок
    kb = types.InlineKeyboardMarkup(row_width=3)

    #Создаем сами кнопки
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    add_to_cart = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='to_cart')

    #Отслеживание плюса и минуса
    if plus_or_minus == 'increment':
        new_amount = int(amount) + 1
        count = types.InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
    elif plus_or_minus == 'decrement':
        if amount > 1:
            new_amount = int(amount) - 1
            count = types.InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))

    #Добавить кнопки в пространство
    kb.add(minus, count, plus)
    kb.row(back)
    kb.row(add_to_cart)

    return kb

#Кнопки для корзины
def cart_buttons():
    #Создаем пространство для кнопок
    kb = types.InlineKeyboardMarkup(row_width=2)

    #Создаем сами кнопки
    order = types.InlineKeyboardButton(text='Оформить заказ', callback_data='order')
    clear = types.InlineKeyboardButton(text='Очистить корзину', callback_data='clear')
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')

    #Добавляем кнопки в пространство
    kb.add(clear, order, back)

    return kb

