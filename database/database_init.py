import mysql.connector
from configs.config import load_config
import os
import logging
import traceback
import mysql.connector


class NoFoundBook(BaseException):
    pass

class NoFoundUser(BaseException):
    pass

class InvalidID(BaseException):
    pass

logger = logging.getLogger(__name__)

path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\configs\\.env"
config = load_config(path_config)


def create_connect():
    connect = mysql.connector.connect(user=config.database.admin,
                          password=config.database.password,
                          host=config.database.host,
                          database=config.database.database)
    cursor = connect.cursor()   
    return connect, cursor

def terminate_connect(connect):
    connect.close()

def _full_checking_database():
    connect, cursor = create_connect()
    cursor.execute("SELECT user_id FROM user")
    users_ids = set(*cursor.fetchall())
    logger.debug(f"id пользователей: {users_ids}")
    ids_in_drct = set(map(lambda x: int(x), os.listdir(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\database\\users_books"))) 
    logger.debug(f"id пользователей в директории: {ids_in_drct}")
    if ids_in_drct == users_ids:
        pass
    else:
        msg = "Некоторые пользователи не найдены в базе данных. Выполните диагностику."
        raise NoFoundUser(msg)

    cursor.execute("SELECT user_id, path FROM book")
    user_id_and_books = cursor.fetchall()
    for i in range(len(user_id_and_books)):
        logger.debug(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\database\\users_books\\{user_id_and_books[i][0]}")
        books = set(os.listdir(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\database\\users_books\\{user_id_and_books[i][0]}"))
        logger.debug(f"Список книг в папке: {books}")
        indx = user_id_and_books[i][1].rfind("/")
        book_name_from_data = user_id_and_books[i][1][indx + 1:]
        if book_name_from_data in books:
            pass
        else:
            msg = f"Некоторые книги не найдены в базе данных. Выполните диагностику."
            raise NoFoundBook(msg)

        
def _add_admins():
    connect, cursor = create_connect()
    admin_lst = config.admin_lst.admins[1:-1]
    if len(admin_lst) == 1:
        logger.warning("Администатор программы не назначен. Назначьте администратора или будет потеряно управление.")
    else:
        admin_lst = set(admin_lst.split(","))
        for admin_id in admin_lst:
            try:
                int(admin_id)
            except ValueError:
                msg = 'ADMIN ID должно быть целое число или None. Проверьте поле ADMIN ID.'
                raise InvalidID(msg)

            try:
                sql_query = '''INSERT INTO user (user_id, role) VALUES(%s, "ADMIN")'''
                cursor.execute(sql_query, (int(admin_id),))
                connect.commit()
            except mysql.connector.errors.IntegrityError:
                pass
            
            
            try:
                os.mkdir(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\database\\users_books\\{admin_id}")
            except FileExistsError:
                pass
    terminate_connect(connect)

def init_database():
    
    connect, cursor = create_connect()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id BIGINT NOT NULL UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS book (book_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,"
                                                     "user_id BIGINT NOT NULL, FOREIGN KEY (user_id) REFERENCES user(user_id),"
                                                     "path VARCHAR(200) UNIQUE NOT NULL,"
                                                     "page INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user_access (user_id BIGINT NOT NULL,"
                                                           "full_name VARCHAR(100))")
    connect.commit()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        os.mkdir("users_books")
    except FileExistsError:
        pass
    
    _full_checking_database()
    _add_admins()
    terminate_connect(connect)

