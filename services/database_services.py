from database.database_init import create_connect, terminate_connect

def delete_book_from_sql(callback):
    connect, cursor = create_connect()
    sql_select = '''DELETE FROM book WHERE user_id = %s and path = %s'''
    user_id = callback.from_user.id
    lst = str(callback.data).split("_")
    book_name_json = lst[1]
    path = f"C:/Users/Lena/Desktop/github proects/book_bot/database/users_books/{user_id}/{book_name_json}"
    cursor.execute(sql_select, (user_id, path))
    connect.commit()
    terminate_connect(connect)