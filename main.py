import telebot, database as db, buttons as bt
from geopy import Nominatim

#Подключение к боту
bot = telebot.TeleBot('6618128660:AAEeH5e4x1rVNqpntvGbyzLW7Tj3w-lRpac')
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

#Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    user_id = message.from_user.id
    #Проверка на наличие юзера в бд
    check_user = db.checker(user_id)
    if check_user:
        products = db.get_pr_name_id()
        bot.send_message(user_id, 'Добро пожаловать!', reply_markup=bt.remove())
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=bt.main_menu_buttons(products))
    else:
        bot.send_message(user_id, 'Приветствую вас! Начнем регистрацию, напишите свое имя', reply_markup=bt.remove())
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

#Запуск бота
bot.polling(non_stop=True)

