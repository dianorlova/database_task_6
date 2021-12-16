from contextlib import closing

import psycopg2

from library.new_main_window import *


if __name__ == '__main__':
    with closing(psycopg2.connect(user="postgres",
                                  password="orlova",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="orlovaDB")) as connection:
        main_window(connection)

