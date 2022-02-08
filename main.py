from time import sleep
from dadata import Dadata
from db_functions import *
from dadata_client import *


def main():
    # Основная программа
    print("\nЗдравствуйте! Я Dadata клиент, я могу указать географические широту и долготу!\nДавайте начнем!\n")
    config = auth() # берем из функции словарь с данными о клиенте
    print("\n")
    client = get_client(config['token'], config['secret']) # передаем API-ключ и Секретный ключ чтобы создать объект DadataClient
    event_loop(client, config['lang']) # основный цикл где происходит вся работа



if __name__ == '__main__':
    main()
