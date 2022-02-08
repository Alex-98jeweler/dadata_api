from dadata import Dadata


def get_client(token, secret):
    client = Dadata(token, secret)
    return client


def event_loop(client, language):
    flag = 1
    mode = 1
    query = input("Введите запрос(формат - город, улица, номер дома, номер квартиры | 'off' - выйти из клиента) :\n>>> ")
    while mode == 1:
        if query == 'off':
            print("До скорой встречи!")
            break
        while flag == 1:
            if query == 'off':
                print("До скорой встречи!")
                break
            res = client.suggest('address', query)
            if len(res) > 0:
                print("Есть ли необходимое значение в списке?")
                for i in range(len(res)):
                    print(f"{i + 1}. {res[i]['value']}")

                number = input("0 - нет и ввести запрос заново, номер значения - да\n>>> ")
                print('\n')
                try:
                    number = int(number)
                except ValueError as error:
                    if len(res) > 1:
                        print(f"Ошибка! Введите число от 1 до {len(res)}")
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
        print(f"Адрес: {result['result']}, Долгота: {result['geo_lon']}, широта: {result['geo_lat']}")
        repeat = input("Продолжим?(да/нет)\n>>> ")
        if repeat == 'нет':
            mode = 0
        else:
            query = input("Введите запрос(формат - город, улица, номер дома, номер квартиры | 'off' - выйти из клиента) :\n>>> ")
            flag = 1





