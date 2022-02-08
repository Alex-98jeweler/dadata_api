from time import sleep
from dadata import Dadata
from db_functions import *
from dadata_client import *


def main():
    print("\nЗдравствуйте! Я Dadata клиент, я могу указать географические широту и долготу!\nДавайте начнем!\n")
    config = auth()
    print("\n")
    client = get_client(config['token'], config['secret'])
    event_loop(client, config['lang'])



if __name__ == '__main__':
    main()
