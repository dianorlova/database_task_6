import tkinter as tk
from tkinter import messagebox as mb, ttk
from tkinter import *

from library.add_product import *
from library.table_database import *


class About(tk.Toplevel):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.label = tk.Text(self,
                             width=50, height=25, borderwidth=3,
                             font=("Comic Sans MS", 14),
                             bg="gray16", fg="white")
        self.label.insert(1.0, text)
        self.label.configure(state="disabled")
        self.label.pack()


# создание главного окна приложения
def main_window(connection):
    app = tk.Tk()
    app.geometry("800x750+350+0")
    app.title("Библиотека программных продуктов")
    app["bg"] = "gray16"

    # создание окна с ошибкой
    def onError(error_message):
        mb.showerror("Ошибка", error_message)

    # преобразование массива одномерно массива продукта в строку
    def to_str(data_list):
        string = ""
        for i in range(len(data_list)):
            string = string + "> Название продукта: " + str(data_list[i][1]) + \
                     "\n  Категория функциональности: " + str(data_list[i][2]) \
                     + "\n  Производитель: " + str(data_list[i][3]) + "\n  Характеристики: " + str(data_list[i][4]) \
                     + "\n  Размер на диске(МБ): " + str(data_list[i][5]) \
                     + "\n  Стоимость продукта(руб): " + str(data_list[i][6]) + "\n  Расположение продукта: " \
                     + str(data_list[i][7]) + "\n"
        return string

    # создание окна приложения для добавления нового продукта
    def create_new_window():
        createNewWindow(connection, app)

    # создание окна приложения с таблицей из базы данных
    def create_table(_):
        createTable(connection, app)

    # метод для создания списка категорий функциональностей
    def create_functions_for_listbox(connection):
        data_list = create_category_list(connection)
        new = []
        for i in range(len(data_list)):
            for j in range(len(data_list[i])):  # столбцы (в данном случае, столбец один)
                new.append(data_list[i][j])  # j = 1 (data_list это двумерный массив (таблица из N строк и 1 столбца))
        new = list(set(new))  # создание списка уникальных(!) категорий функциональностей
        new.sort()  # сортируем список в лексикографическом порядке
        return new

    # метод для замены id производителя на имя производителя
    def change_provider_id_to_name(data_list):
        for i in range(len(data_list)):
            provider_name = get_provider_name(connection, data_list[i][3])
            data_list[i][3] = provider_name[0][0]
        return data_list

    # настройка полей ввода для поиска продукта
    f_top = Frame(app)
    tk.Label(f_top,
             text="Библиотека программных продуктов",
             font=("Comic Sans MS", 24),
             bg="gray16", fg="orchid1").pack()
    f_top.pack(pady=30)

    tk.Label(app,
             text="Введите название продукта",
             font=("Comic Sans MS", 18),
             bg="gray16", fg="white").pack()
    product_name = tk.Entry(app, font="Arial 18", width=20)
    product_name.pack(pady=10)

    tk.Label(app,
             text="Выберите категорию функциональности продукта",
             font=("Comic Sans MS", 18),
             bg="gray16", fg="white").pack()

    # в category располагаются(в виде таблицы из 1 столбца и N строк)все категории функциональностей из таблицы library
    category = create_functions_for_listbox(connection)

    # заполнение значениями лист-бокса категорий функциональности
    lb = Listbox(app, font=("Comic Sans MS", 16), height=6)
    for i in category:
        lb.insert(END, i)

    lb.bind("<<ListboxSelect>>")
    lb.pack(pady=10)

    tk.Label(app,
             text="Введите имя производителя продукта",
             font=("Comic Sans MS", 18),
             bg="gray16", fg="white").pack()
    product_provider = tk.Entry(app, font="Arial 18", width=20)
    product_provider.pack(pady=10)

    found = tk.Button(app,
                      text="Найти!",
                      font=("Comic Sans MS", 14, "bold"),
                      bg="lightblue", width=15,
                      height=1)

    # метод для поиска продукта
    def find(_):
        # проверяем правильность заполнения полей
        if product_name.get() == "" or lb.get(ANCHOR) == "" or product_provider.get() == "":
            onError("Не заполнены необходимые поля")
        else:
            try:
                # получаем id производителя из таблицы providers по имени производителя
                provider_id = get_provider_id(connection, product_provider.get())

                # создаем список продуктов-результатов поиска
                data_list1 = find_local(connection, product_name.get(), lb.get(ANCHOR), provider_id[0][0])

                # проверяем что список продуктов-результатов не пустой
                if len(data_list1) == 0:
                    onError("Продукт не найден!\n\nПроверьте правильность заполнения полей." +
                            " В частности, название продукта должно быть уникальным.\n\n" +
                            "Для получения информации о текущей БД щёлкните на кнопку \"Показать базу данных\"" +
                            " на главном окне приложения.")
                else:
                    # если не пустой выполняем поиск аналогов и вывод результатов
                    data_list2 = find_category(connection, lb.get(ANCHOR))

                    # меняем значения производителя в продукте-результате поиска для красивого вывода
                    data_list1 = change_provider_id_to_name(data_list1)

                    # меняем значения производителя в аналогах поиска для красивого вывода
                    data_list2 = change_provider_id_to_name(data_list2)

                    # создаем новое окно с красивым выводом результатов поиска продукта и аналогов
                    return About(app,
                                 "Найденный продукт:\n" + to_str(data_list1) + "\n\nАналоги:\n" + to_str(data_list2))
            except:
                onError("Ошибка запроса к БД. Проверьте правильность заполнения полей")

    found.bind('<Button-1>', find)
    found.pack(pady=15)

    add_product = tk.Button(app,
                            text="Добавить продукт",
                            font=("Comic Sans MS", 14, "bold"),
                            bg="lightgreen",
                            width=15, height=1,
                            command=create_new_window)
    add_product.pack()

    btn_show_table = tk.Button(text="Показать базу данных",
                               font=("Comic Sans MS", 14, "bold"),
                               bg="orchid1",
                               width=20, height=1)

    btn_show_table.bind('<Button-1>', create_table)
    btn_show_table.pack(pady=15)

    app.mainloop()
