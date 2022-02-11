import sqlite3

class DB:
    '''
    Класс для взаимодействия с базой даннох для чтения и записи БД.
    '''
    __create_query  = \
            '''
            CREATE TABLE settings (
            id INTEGER NOT NULL PRIMARY KEY,
            token VARCHAR(200) NOT NULL,
            language VARCHAR(2) NOT NULL,
            secret VARCHAR(200)
            );

            '''
    __insert_query = \
            '''
            INSERT INTO settings VALUES(1, '{}', '{}', '{}');

            '''

    def __init__(self, name) -> None:
        self.connection = sqlite3.connect(name)
        self.curs = self.connection.cursor()
   
    def get_config(self) -> dict:
        '''
        Получение настроек из БД. Возвращает словарь с необходимыми значениями
        '''
        config = {
            'token': None, 
            'lang': None, 
            'secret' : None
        }
        res = self.curs.execute('select * from settings;').fetchall()
        config['token'] = res[0][1]
        config['lang'] = res[0][2]
        config['secret'] = res[0][3]

        return config
    
    def check_db(self) -> bool:
        '''
        Проверяет есть ли в БД записи. Возвращает True если есть.
        '''
        checked = False

        try:
            res = self.curs.execute('select * from settings;').fetchall()
        except sqlite3.OperationalError:
            self.curs.execute(self.__create_query)
            self.connection.commit()
        else:
            if len(res) > 0:
                checked = True
        return checked


    def add_info(self, token: str, lang: str, secret: str):
        self.curs.execute(self.__insert_query.format(token, lang, secret))
        self.connection.commit()
        
