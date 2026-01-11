import json
import os

def append_db(user_id) -> None:
    '''Эта функция добавляет пользователя в базу данных, если его там нет а также создает персональную папку для него'''
    user_id = str(user_id)
    
    file = open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "r+", encoding="utf-8")
    data = json.load(file)
    if checking_db(user_id, data):
        file.close()
    else:   
        anti_acess(user_id) 
        data[user_id] = init_db()
        file.seek(0)
        json.dump(data, file, indent=2)
        file.close()
        os.chdir("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books")
        os.mkdir(user_id)
        


def checking_db(user_id, base_data) -> bool:
    '''Проверяет наличие пользователя в базе данных'''
    if user_id in base_data.keys():
        return True
    else:
        return False

def init_db() -> dict:
    '''Возвращает пустой словарь нового пользователя'''
    return {}
        
def append_path(user_id, path):
    '''Создает базовый словарь пользователя хотя бы с одной книгой'''
    file = open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "r+", encoding="utf-8")
    data = json.load(file)
    data[str(user_id)][path.split('\\')[-1]] = {"path_book" : "", "page" : 1, "bookmarks" : []}
    data[str(user_id)][path.split('\\')[-1]]["path_book"] = path
    file.close()

    with open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    
    

    





def anti_acess(user_id):
    'До создания антивируса функция блокирует пользователей с чужим id'
    if user_id != "6027578907" and user_id != "1898019149" and user_id != "5215143463":
       raise ValueError(f"Несанкционированный доступ: id = {user_id}")

