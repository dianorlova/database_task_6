from contextlib import closing

import psycopg2

from library.new_main_window import *


if __name__ == '__main__':
    with closing(psycopg2.connect(user="postgres",
                                  password="Max_sw1mm",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="tikhomirovBD")) as connection:
        main_window(connection)

