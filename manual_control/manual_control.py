import sys
import os
import json

# Добавляем корневую директорию проекта в путь поиска модулей
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


path_settings = os.path.dirname(os.path.abspath(__file__)) + "\\settings.json"
with open(path_settings, "r", encoding="utf-8") as file:
    settings = json.load(file)
    language = settings["language"]


if language == "English":
    from  lexicons.lexicon_for_terminal_ENG import lexicon_ENG as lexicon
elif language == "Russian":
    from  lexicons.lexicon_for_terminal_RU import lexicon_RU as lexicon



from database.database_init import create_connect, terminate_connect
from mysql.connector.errors import IntegrityError





print(lexicon["start"])
while True:
    command = input("book_bot> ")
    while True:
        
        if command == "add":
            sql_query = '''INSERT INTO user_acess
               (user_id, full_name)
               VALUES(%s, %s)'''
            connect, cursor = create_connect()
            
            try:
                user_id = int(input("user_id = "))
            
            except ValueError:
                print("TypeError: value must be integer")
                terminate_connect(connect)
                continue
            
            full_name = input("user_name = ")
            try:
                cursor.execute(sql_query, (user_id, full_name[:-1]))
                connect.commit()
                print(lexicon["user_added"])
                break
            except IntegrityError as e:
                print(f"DatabaseError: {e} ")
                break


        elif command == "del":
            sql_query = '''DELETE FROM user_acess WHERE user_id = %s'''
            connect, cursor = create_connect()
            try:
                user_id = int(input("user_id = "))
            
            except ValueError:
                print("TypeError: value must be integer")
                terminate_connect(connect)
                continue
            try:
                cursor.execute(sql_query, (user_id,))
            except IntegrityError as e:
                print(f"DatabaseError: {e} ")
                break

        elif command == "help":
            print(lexicon["help"])
            break
        
        elif command == "change_language":
            lg = input(lexicon["change_lg"])
            if lg == "Russian":
                with open(path_settings, "r+", encoding="utf-8") as file:
                    data = json.load(file)
                    data["language"] = "Russian"
                    file.seek(0)
                    json.dump(data, file)
                print(lexicon["changed_lg"])
            
            
            elif lg == "English":
                with open(path_settings, "r+", encoding="utf-8") as file:
                    data = json.load(file)
                    data["language"] = "English"
                    file.seek(0)
                    json.dump(data, file)
                print(lexicon["changed_lg"])
            
            break

            


        else:
            break

        