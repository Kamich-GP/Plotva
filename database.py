import sqlite3

#Подключение к базе данных
connection = sqlite3.connect('database.db', check_same_thread=False)
#Связь SQL с Python
sql = connection.cursor()


#Создание таблицы пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER,'
            'name TEXT,'
            'num TEXT,'
            'loc TEXT);')
#Создание таблицы продуктов
sql.execute('CREATE TABLE IF NOT EXISTS products'
            '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'pr_name TEXT,'
            'pr_amount INTEGER,'
            'pr_price REAL,'
            'pr_des TEXT,'
            'pr_photo TEXT);')
#Создание таблицы корзины
sql.execute('CREATE TABLE IF NOT EXISTS cart'
            '(user_id INTEGER,'
            'user_product TEXT,'
            'product_quantity INTEGER,'
            'total REAL);')

##Методы для пользователей##
#Регистрация
def register(id, name, num, loc):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, num, loc))
    #Фиксируем изменения
    connection.commit()

#Проверка на наличие пользователя в базе
def checker(id):
    check = sql.execute('SELECT id FROM users WHERE id=?;', (id,))

    if check.fetchone():
        return True
    else:
        return False

##Методы для продуктов##
#Добавление продукта в базу данных
def add_product(pr_name, pr_amount, pr_price, pr_des, pr_photo):
    sql.execute('INSERT INTO products'
                '(pr_name,'
                'pr_amount,'
                'pr_price,'
                'pr_des,'
                'pr_photo) VALUES (?,?,?,?,?);',
                (pr_name, pr_amount, pr_price, pr_des, pr_photo))
    #Фиксируем изменения
    connection.commit()

#Вывод информации об определенном продукте
def show_info(pr_id):
    sql.execute('SELECT pr_name, pr_amount, pr_price, pr_des, pr_photo'
                'FROM products WHERE id=?;', (pr_id,)).fetchone()

#Вывод всех продуктов из базы
def show_all_products():
    all_products = sql.execute('SELECT * FROM products;')

    return all_products.fetchall()

#Вывод id продуктов
def get_pr_name_id():
    products = sql.execute('SELECT id, pr_name, pr_amount, pr_price FROM products;').fetchall()

    return products

#Получить имя продукта
def get_pr_name(id):
    product = sql.execute('SELECT pr_name FROM products WHERE id=?', (id,))
    return product.fetchone()
def get_pr_id():
    prods = sql.execute('SELECT id, pr_name, pr_amount FROM products;').fetchall()
    sorted_prods = [i[0] for i in prods if i[2] > 0]
    return sorted_prods

##Методы для корзины##
#Добавление товаров в корзину
def add_to_cart(user_id, pr_name, pr_quantity, user_total=0):
    sql.execute('INSERT INTO cart(user_id, user_product, product_quantity, total)'
                'VALUES(?,?,?,?);', (user_id, pr_name, pr_quantity, user_total))
    # Фиксируем изменения
    connection.commit()
    amount = sql.execute('SELECT pr_amount FROM products WHERE pr_name=?;', (pr_name,)).fetchone()
    sql.execute(f'UPDATE products SET pr_amount={amount[0] - pr_quantity} '
                f'WHERE pr_name=?;', (pr_name,))
    #Фиксируем изменения
    connection.commit()

#Очистка корзины
def del_cart(user_id):
    pr_name = sql.execute('SELECT user_product FROM cart WHERE user_id=?;', (user_id,)).fetchone()
    amount = sql.execute('SELECT pr_amount FROM products WHERE pr_name=?;', (pr_name[0],)).fetchone()[0]
    pr_quantity = sql.execute('SELECT product_quantity FROM cart WHERE user_id=?;', (user_id,)).fetchone()[0]
    sql.execute(f'UPDATE products SET pr_amount={amount + pr_quantity} WHERE pr_name=?;', (pr_name,))
    # Фиксируем изменения
    connection.commit()
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))
    #Фиксируем изменения
    connection.commit()

#Отображение корзины
def show_cart(user_id):
    cart = sql.execute('SELECT user_product, product_quantity, total FROM cart WHERE user_id=?;', (user_id,))
    return cart.fetchone()
