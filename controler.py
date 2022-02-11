from dadata_client import DadataClient
from database import DB

'''
Модуль с основной логикой программы.
'''

db = DB('settings.db') # инициируем объект базы данных

def show_menu(menu: list) -> int:
    '''
        Принимает на вход список строк необходимого меню, нумирует и отображает 
        значения меню. Возвращает число которое вводит пользователь.
    '''
    for i in range(len(menu)):
        print(f"{i + 1}. {menu[i]}")
    print('0. Выход')
    choose = int(input('>>> '))

    return choose

def check_token(token : str) -> bool:
    '''Проверяет доступность токена. Возвращает True если доступен, и False если нет'''

    res = False
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
    if request.status_code == 200:
        res = True
        
    return res

def print_suggestions(suggestions: list) -> str:
    '''отображает подсказки в виде меню. отображает заново если введено число больше допустимого диапазона'''

    if len(suggestions) > 0:
        choose = show_menu(suggestions)
    else:
        print("По вашему запросу ничего не найдено")
        print('\n0. Назад')
        choose = int(input('>>> '))
    result = None
    if choose == 0:
        result = -1
    elif choose > len(suggestions):
        print('Ошибка введите из выбранного')
        return print_suggestions(suggestions)
    else:
        result = suggestions[choose - 1]
    return  result

def input_add_data():
    '''Запрашивает ввод данных, и добавляет их в БД для дальнейшей работы'''

    for i in range(3, 0, -1):
            token = input(f"Введите API ключ({i} попыток осталось)\n>>> ")
            if check_token(token):
                secret = input(f"Введите секретный ключ({i} попыток осталось)\n>>> ")
                lang = input("Введите язык отображения подсказок(ru - русский, en - английский)\n>>> ")
                db.add_info(token, lang, secret)
                break
            else:
                print("API ключ не валиден")

def check_main_menu(number, client):
    '''Логика работы главного меню'''
    if number == 1:
        query = input('Введите ваш запрос(город, улица, номера дома и квартиры)\n>>> ')
        suggestions = client.get_suggestions(query)
        address = print_suggestions(suggestions)
        if address == -1:
            pass
        else:
            print(client.get_geolocate(address))
    if number > 1:
        print("Такой команды нету или находится в разработке")


def run():
    '''
    Основная логика в которой выполняется основная программа.
    '''
    config = None # инициализируем переменную 

    if db.check_db() == False: # проверяем записи в БД, если нет то запросим их ввод и объект БД занесет их
        print("Здравствуйте! Я Dadata-Client, я помогу Вам получить информацию из баз Dadata.\nДля начала работы введите следующие данные:")
        input_add_data()
    else: 
        print("Рад что вы вернулись! Продолжим?")

    config = db.get_config() # получаем из БД конфигурацию
    client = DadataClient(config['token'], config['secret'], config['lang']) # инициируем объект клиента Dadata
    menu = ['Найти географические координаты'] # список главного меню
    choose = show_menu(menu) # отображаем список в виде пронумерованного меню

    while choose != 0: # основной цикл программы
        check_main_menu(choose, client)
        choose = show_menu(menu)

    db.connection.close()

        
