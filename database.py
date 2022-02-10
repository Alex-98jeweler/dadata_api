import sqlite3

class DB:

    def __init__(self, name) -> None:
        connection = sqlite3.connect(name)
        self.curs = connection.cursor()

class DB_Reader(DB):
    
    def get_config(self) -> dict:
        config = {
            'token': None, 
            'lang': None, 
            'secret' : None
        }
        res = self.curs.execute('select * from settings;').fetchall()
        config['token'] = res[0][1]
        config['lang'] = res[0][2]
        config['config'] = res[0][3]
        self.curs.close()

        return config


class DB_Writer(DB):

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
       
    def check_db(self) -> bool:
        checked = False

        try:
            res = self.curs.execute('select * from settings;').fetchall()
        except sqlite3.OperationalError:
            self.curs.execute(self.__create_query)
        else:
            if len(res) > 0:
                checked = True

        return checked


    def add_info(self, token: str, lang: str, secret: str):
        self.curs.execute(self.__insert_query.format(token, lang, secret))
