import sqlite3
from time import sleep

def set_connection():
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
    return connection


def check_in_db(token):
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
    conn = set_connection()
    curs = conn.cursor()
    id = get_last_id(curs)
    curs.execute(f"INSERT INTO info VALUES({id}, '{token}', '{language}', '{secret}');")
    conn.commit()
    curs.close()


def get_last_id(curs):
    id = 0
    res = curs.execute("SELECT * FROM info;").fetchall()
    if len(res) == 0:
        id = 1
    else:
        id = res[-1][0] + 1
    return id


def check_token(token : str):
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
    for i in range(3, 0, -1):
        token = input(f"Enter your token(you have {i} attempts): \n>>>")
        sleep(2)
        if check_token(token) == 0:
            check = check_in_db(token)
            if check['status'] == 0:
                language = check['lang']
                secret = check['secret']
                print('Authorization is successful!')
                break
            else:
                language = input("Enter preferred language(ru - Russian, en - English): ")
                secret = input("Введите ваш 'Секретный ключ' по адресу\nhttps://dadata.ru/profile/#info (Ctrl + клик по ссылке)\n")
                add_data(token, language, secret)
                print("You're registered! Good luck!")
                break
        else:
            print("This token is not authorized, enter your token again.\n")
    
    return {'token': token, 'lang':language, 'secret': secret}
