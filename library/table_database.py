import tkinter as tk
from tkinter import ttk
from tkinter import *

from library.products import *


def createTable(connection, app):
    wnd_show_table = tk.Toplevel(app)
    wnd_show_table["bg"] = "gray16"
    wnd_show_table.title("База данных")
    wnd_show_table.geometry("1200x300+150+50")

    table_frame = tk.Frame(wnd_show_table)

    table = ttk.Treeview(table_frame, show="headings")

    table_scroll = Scrollbar(wnd_show_table)
    table_scroll.pack(side=RIGHT, fill=Y)

    table.configure(yscrollcommand=table_scroll.set, xscrollcommand=table_scroll.set)

    table_scroll.config(command=table.yview)
    table_scroll.config(command=table.xview)

    heads = ['ID продукта', 'Название', 'Категория функциональности', 'Производитель', 'Характеристика',
             'Размер на жестком диске (МБ)', 'Стоимость (руб)', 'Расположение']

    table['columns'] = heads
    for header in heads:
        table.heading(header, text=header, anchor='center')
        if header == 'ID продукта' or header == 'Название':
            table.column(header, anchor='center', width=40)
        elif header == 'Категория функциональности' or header == 'Размер на жестком диске (МБ)':
            table.column(header, anchor='center', width=90)
        else:
            table.column(header, anchor='center', width=50)

    data_list3 = output_all_in_table(connection)

    for i in range(len(data_list3)):
        provider_name = get_provider_name(connection, data_list3[i][3])
        data_list3[i][3] = provider_name

    for row in data_list3:
        table.insert('', END, values=row)

    table.pack(expand=YES, fill=BOTH)
    table_frame.pack(expand=YES, fill=BOTH)
