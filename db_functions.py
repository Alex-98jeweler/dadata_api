import sqlite3
from time import sleep

def set_connection():
    '''
    Устанавливает соединение с базой данных. Пробует сделать запрос к таблице.
    Если таблица существует, то ничего не происходит, если таблицы нет, то создает ее.
    Возвращает объект подключения к базе данных. 
    '''
    connection = sqlite3.connect("settings.db")
    curs = connection.cursor()
    try:
        res = curs.execute("SELECT * FROM info;")
    except sqlite3.OperationalError as error:
        curs.execute('''CREATE TABLE IF NOT EXISTS info (
            id INTEGER PRIMARY KEY NOT NULL,
            token varchar(200),
            language VARCHAR(2),
            secret VARCHAR(200)
        );''')
        connection.commit()
    return connection


def check_in_db(token):
    '''
    Проверяет введеные данные в основной программе. Если уже есть в БД, то возвращает словарь 
    с соответствующими языком и секретным ключом и статусом проверки.
    Статус 1 - нет в бд
    Статус 2 - есть в бд
    
    '''
    res = {'status': 1, 'lang': None, 'secret' : None}
    conn = set_connection()
    curs = conn.cursor()
    data = curs.execute("SELECT * FROM info;").fetchall()
    for i in range(len(data)):
        if token in data[i]:
            res['status'] = 0
            res['lang'] = data[i][2]
            res['secret'] = data[i][3]
            break
    curs.close()
    return res


def add_data(token, language, secret):
    '''
    Добавляет данные в таблицу в бд.    
    '''
    conn = set_connection()
    curs = conn.cursor()
    id = get_last_id(curs)
    curs.execute(f"INSERT INTO info VALUES({id}, '{token}', '{language}', '{secret}');")
    conn.commit()
    curs.close()


def get_last_id(curs):
    '''
        Получает ID последней записи и возвращает ID который необходимо записать. 
    '''
    id = 0
    res = curs.execute("SELECT * FROM info;").fetchall()
    if len(res) == 0:
        id = 1
    else:
        id = res[-1][0] + 1
    return id


def check_token(token : str):
    '''
        Делает пробный запрос к серверу. Проверяет статус код запроса.
        Если код 200, функция возвращает 0, тем самым подтверждая валидность
        API-ключа. Возвращает 1 если статус код запроса отличен от 200. 
    '''

    res = 0
    import requests
    import json
    HEADEARS = {
        'Authorization': 'Token {}'.format(token),
        'Content-Type':'application/json',
        'Accept': 'application/json'
    }
    url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address'
    data = {'query': 'check'}
    request = requests.post(url=url, headers=HEADEARS, data = json.dumps(data))
    if request.status_code != 200:
        res = 1
    return res


def auth():
    '''
    Функция авторизации. Запрашивает ввод API-ключа. Если такой уже есть в базе данных,
    то записывает соответствующие язык и секретный ключ в словарь. Если API-ключа нет в базе данных,
    то просит ввести препдпочтительный язык и секретный ключ, после ввода заносит информацию в БД.
    Возвращает словарь в котором записаны токен, язык и секретный ключ. 
    '''
    for i in range(3, 0, -1):
        token = input(f"Введите ваш 'API-ключ'(Попытка {i})\nЕго можно найти по адресу https://dadata.ru/profile/#info (Ctrl + клик по ссылке)\n>>> ")
        sleep(2)
        print('\n')
        # делаем проверку на валидность токена
        if check_token(token) == 0:
            # делаем проверку на нахождение токена в БД
            check = check_in_db(token)
            if check['status'] == 0: # если токен есть в базе данных то присваиваем переменным language и secret соответствующие значения из словаря check
                language = check['lang']
                secret = check['secret']
                print('Авторизация прошла успешно! Вы в эфире!\n')
                break
            else:
                # если нет то просим их ввести и заносим в базу данных.
                print("Я вижу что Ваш API-ключ рабочий, но нужно дополнить информацию о Вас.\n")
                language = input("Введите язык на котором хотели бы получать названия городов(ru - русский, en - английский)\n>>> ")
                print("\n")
                secret = input("Введите ваш 'Секретный ключ'\nЕго можно найти по адресу https://dadata.ru/profile/#info (Ctrl + клик по ссылке)\n>>> ")
                print('\n')
                add_data(token, language, secret)
                print("Информация дополнена! Вы в эфире!\n")
                break
        else: # если токен невалидный, то пишем ошибку 
            print("Упс, произошла ошибка. Убедитесь что API-ключ зарегистрирован на ресурсе и введен правильно.\n")
            
    
    return {'token': token, 'lang':language, 'secret': secret}
