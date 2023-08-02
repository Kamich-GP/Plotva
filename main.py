import telebot, database as db, buttons as bt
from telebot.types import ReplyKeyboardRemove as remove
from geopy import Nominatim

#Подключение к боту
bot = telebot.TeleBot('')
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
#Временные данные
users = {}
#Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    user_id = message.from_user.id
    #Проверка на наличие юзера в бд
    check_user = db.checker(user_id)
    if check_user:
        products = db.get_pr_name_id()
        bot.send_message(user_id, 'Добро пожаловать!', reply_markup=remove())
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=bt.main_menu_buttons(products))
    else:
        bot.send_message(user_id, 'Приветствую вас! Начнем регистрацию, напишите свое имя', reply_markup=remove())
        #Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)

#Этап получения имени
def get_name(message):
    user_name = message.text
    bot.send_message(user_id, 'Отлично! А теперь отправьте номер!',
                     reply_markup=bt.num_button())
    #Этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)
#Этап получения локации
def get_num(message, user_name):
    #Если нажал на кнопку
    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, 'А теперь отправьте локацию!',
                         reply_markup=bt.loc_button())
        #Переход на этап получения локации
        bot.register_next_step_handler(message, get_loc, user_name, user_num)
    #Если не нажимал кнопку
    else:
        bot.send_message(user_id, 'Отправьте свой контакт через кнопку!')
        bot.register_next_step_handler(message, get_num, user_name)


#Функция выбора количества товара
@bot.callback_query_handler(lambda call: call.data in ['back', 'to_cart', 'increment', 'decrement'])
def get_user_count(call):
    chat_id = call.message.chat.id

    if call.data == 'increment':
        count = users[chat_id]['pr_amount']

        users[chat_id]['pr_amount'] += 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id,
                              reply_markup=bt.choose_product_count(count, 'increment'))
    elif call.data == 'decrement':
        count = users[chat_id]['pr_amount']

        users[chat_id]['pr_amount'] -= 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id,
                                      reply_markup=bt.choose_product_count(count, 'decrement'))
    elif call.data == 'back':
        products = db.get_pr_name_id()

        bot.edit_message_text('Выберите пункт меню:', chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=bt.main_menu_buttons(products))
    elif call.data == 'to_cart':
        products = db.get_pr_name_id()
        product_count = users[chat_id]['pr_amount']
        user_total = products[0][3] * product_count
        user_product = db.get_pr_name(users[chat_id]['pr_name'])

        db.add_to_cart(chat_id, user_product[0], product_count, user_total)
        bot.edit_message_text('Ваш товар был добавлен в корзину! Хотите заказать что-то еще?',
                              chat_id=chat_id, message_id=call.message.message_id,
                              reply_markup=bt.main_menu_buttons(products))

#Корзина
@bot.callback_query_handler(lambda call: call.data in ['cart', 'order', 'clear', 'back'])
def cart_handle(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    products = db.get_pr_name_id()

    if call.data == 'clear':
        db.del_cart(user_id)
        bot.edit_message_text('Корзина очищена! Желаете что-то еще?', chat_id=chat_id,
                              message_id=message_id, reply_markup=bt.main_menu_buttons(products))
    elif call.data == 'order':
        bot.send_message(791555605, 'Новый заказ!')
        db.del_cart(user_id)
        bot.edit_message_text('Заказ был оформлен и скоро будет доставлен! Желаете заказать что-то еще?',
                              chat_id=chat_id, message_id=message_id,
                              reply_markup=bt.main_menu_buttons(products))
    elif call.data == 'back':
        bot.edit_message_text('Выберите пункт меню:', chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=bt.main_menu_buttons(products))
    elif call.data == 'cart':
        text = db.show_cart(user_id)
        bot.edit_message_text(f'Корзина:\n{text[0]}', chat_id=chat_id, message_id=message_id,
                              reply_markup=bt.cart_buttons())

#Этап получения локации
def get_loc(message, user_name, user_num):
    #Если нажал на кнопку
    if message.location:
        user_loc = geolocator.reverse(f'{message.location.longitude},'
                                      f'{message.location.latitude}')
        #Регистрируем пользователя
        db.register(user_id, user_name, user_num, user_loc)
        #Перевод на главное меню
        bot.send_message(user_id, 'Вы успешно зарегистрировались!')
        products = db.get_pr_name_id()
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=bt.main_menu_buttons(products))
    #Если не нажал кнопку
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку!')
        bot.register_next_step_handler(message, get_loc, user_name, user_num)
#Функция для выбора количества
@bot.callback_query_handler(lambda call: int(call.data) in db.get_pr_id())
def get_user_product(call):
    chat_id = call.message.chat.id
    users[user_id] = {'pr_name': call.data, 'pr_amount': 1}
    message_id = call.message.message_id

    bot.edit_message_text('Выберите количество', chat_id=chat_id, message_id=message_id,
                          reply_markup=bt.choose_product_count())


#Запуск бота
bot.polling(non_stop=True)

