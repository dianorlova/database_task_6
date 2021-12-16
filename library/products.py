def find_local(connection, name, category, provider):
    sql_command = f"""SELECT * FROM library WHERE "product_name" = '{name}'
    AND "product_category" = '{category}' 
    AND "product_provider" = '{provider}';"""
    with connection.cursor() as cursor:
        cursor.execute(sql_command)
        return [list(elem) for elem in cursor]


def add_db_row(connection, name, category, provider, requirements, size, value, path):
    sql_command = f""" INSERT INTO library (product_name, product_category, product_provider, product_requirements, product_size, product_value, product_path)
     VALUES ( '{name}', '{category}', '{provider}', '{requirements}', {size}, {value}, '{path}')"""
    with connection.cursor() as cursor:
        cursor.execute(sql_command)
    connection.commit()


def create_category_list(connection):
    sql_command = f"""SELECT product_category FROM library;"""
    with connection.cursor() as cursor:
        cursor.execute(sql_command)
        return [list(elem) for elem in cursor]


def find_category(connection, category):
    sql_command = f"""SELECT * FROM library WHERE "product_category" = '{category}' ;"""
    with connection.cursor() as cursor:
        cursor.execute(sql_command)
        return [list(elem) for elem in cursor]


def output_all_in_table(connection):
    sql_command = f"""SELECT * FROM library ;"""
    with connection.cursor() as cursor:
        cursor.execute(sql_command)
        return [list(elem) for elem in cursor]
