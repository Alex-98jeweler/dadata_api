from time import sleep
from dadata import Dadata
from db_functions import *
from dadata_client import *


token = '1e6b20fd720f7f75dae41c301b8486ef6fd0db26'
secret = '56d780143aab6946897488eb4e177166bb36594c'

def main():
    print("\nЗдравствуйте! Я Dadata клиент, я могу указать географические широту и долготу!\nДавайте начнем!\n")
    config = auth()
    print("\n")
    client = get_client(config['token'], config['secret'])
    event_loop(client, config['lang'])


    

if __name__ == '__main__':
    main()







