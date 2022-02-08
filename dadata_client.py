from dadata import Dadata


def get_client(token, secret):
    '''
    Возвращает объект класса DadataClient. Принимает на вход API-ключ и Секретный ключ.
    '''
    client = Dadata(token, secret)
    return client


def event_loop(client, language):
    '''
    Здесь происходит програмный цикл. На вход принимает объект DadataClient и язык на котором будет отображаться
    возвращаемый контент.
    '''
    flag = 1 # флаг для внутреннего цикла
    mode = 1 # флаг для внешнего цикла
    query = input("Введите запрос(формат - город, улица, номер дома, номер квартиры | 'off' - выйти из клиента) :\n>>> ")
    while mode == 1: # внешний цикл
        if query == 'off': # выход из цикла
            print("До скорой встречи!")
            break
        while flag == 1: # внутренний цикл
            if query == 'off': # выход из цикла
                print("До скорой встречи!")
                break
            res = client.suggest('address', query) # делаем запрос к серверу
            if len(res) > 0: # если вернул хотя бы одно значение, то печатает подсказки на экране
                print("Есть ли необходимое значение в списке?")
                for i in range(len(res)):
                    print(f"{i + 1}. {res[i]['value']}")
                # если есть искомое значение, то пользователь вводит номер значения, если нету то вводит 0 и вводит заново искомый запрос
                number = input("0 - нет и ввести запрос заново, номер значения - да\n>>> ")
                print('\n')
                try: # обработка исключения если введено не число
                    number = int(number)
                except ValueError as error: # если исключение возникает то программа просит ввести число, а не букву
                    if len(res) > 1:
                        print(f"Ошибка! Введите ЧИСЛО от 1 до {len(res)}")
                        number = input(">>> ")
                        number = int(number)
                    else:
                        print("Введите цифру 1")
                        number = input(">>> ")
                        number = int(number)
                if number == 0:
                    query = input("Введите запрос(город, улица, номер дома, номер квартиры | 'off' - выйти из клиента):\n>>> ")
                else:
                    if number < 0 or number > len(res):
                        print(f"Ошибка! Число находится вне допустимого диапазона! Введите число от 1 до {len(res)}")
                        number = int(input(">>>"))
                    query = res[number - 1]['value']
                    flag = 0
            else:
                print("По вашему запросу ничего не найдено")
                query = input("Введите запрос заново(город, улица, номер дома, номер квартиры | 'off' - выйти из клиента):\n>>> ")
        if query == 'off':
            break
        result = client.clean('address', query)
        print(f"Адрес: {result['result']}, Долгота: {result['geo_lon']}, широта: {result['geo_lat']}") # если все прошло успешно то напечается искомый адрес, его долгота и широта
        repeat = input("Продолжим?(да/нет)\n>>> ")
        if repeat == 'нет':
            mode = 0
        else:
            query = input("Введите запрос(формат - город, улица, номер дома, номер квартиры | 'off' - выйти из клиента) :\n>>> ")
            flag = 1





