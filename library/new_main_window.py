import tkinter as tk
from tkinter import messagebox as mb, ttk
from tkinter import *

from library.products import *


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


def main_window(connection):
    app = tk.Tk()
    app.geometry("800x750+350+0")
    app.title("Библиотека программных продуктов")
    app["bg"] = "gray16"

    def onError(error_message):
        mb.showerror("Ошибка", error_message)

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

    def createNewWindow():

        def onError(error_message):
            mb.showerror("Ошибка", error_message)

        def onInfo(message):
            mb.showinfo("Информация", message)

        newWindow = tk.Toplevel(app)
        newWindow["bg"] = "gray16"
        newWindow.title("Добавление нового продукта")
        newWindow.geometry("600x650+450+50")

        tk.Label(newWindow,
                 text="Введите название продукта",
                 font=("Comic Sans MS", 18),
                 bg="gray16", fg="white").pack(pady=5)
        product_name = tk.Entry(newWindow, font="Arial 18", width=20)
        product_name.pack()

        tk.Label(newWindow,
                 text="Введите категорию функциональности продукта",
                 font=("Comic Sans MS", 18),
                 bg="gray16", fg="white").pack(pady=5)
        product_category = tk.Entry(newWindow, font="Arial 18", width=20)
        product_category.pack()

        tk.Label(newWindow,
                 text="Введите имя производителя продукта",
                 font=("Comic Sans MS", 18),
                 bg="gray16", fg="white").pack(pady=5)
        product_provider = tk.Entry(newWindow, font="Arial 18", width=20)
        product_provider.pack()

        tk.Label(newWindow,
                 text="Введите характеристики продукта",
                 font=("Comic Sans MS", 18),
                 bg="gray16", fg="white").pack(pady=5)
        product_requirements = tk.Entry(newWindow, font="Arial 18", width=20)
        product_requirements.pack()

        tk.Label(newWindow,
                 text="Введите размер продукта на жестком диске, МБ",
                 font=("Comic Sans MS", 18),
                 bg="gray16", fg="white").pack(pady=5)
        product_size = tk.Entry(newWindow, font="Arial 18", width=20)
        product_size.pack()

        tk.Label(newWindow,
                 text="Введите стоимость продукта",
                 font=("Comic Sans MS", 18),
                 bg="gray16", fg="white").pack(pady=5)
        product_value = tk.Entry(newWindow, font="Arial 18", width=20)
        product_value.pack()

        tk.Label(newWindow,
                 text="Введите расположение продукта",
                 font=("Comic Sans MS", 18),
                 bg="gray16", fg="white").pack(pady=5)
        product_path = tk.Entry(newWindow, font="Arial 18", width=20)
        product_path.pack()

        add = tk.Button(newWindow,
                        text="Добавить!",
                        font=("Comic Sans MS", 14, "bold"),
                        bg="lightgreen",
                        width=15, height=1)

        message = "Продукт успешно добавлен в библиотеку"
        error_message = "Ошибка добавления продукта в библиотеку.\n\nЗаполните все поля!"

        def add_product():
            add_db_row(
                connection,
                product_name.get(),
                product_category.get(),
                product_provider.get(),
                product_requirements.get(),
                product_size.get(),
                product_value.get(),
                product_path.get(),
            )

        def check_new_product(_):
            if (product_name.get() == "" or product_category.get() == "" or product_provider.get() == "" or
                    product_requirements.get() == "" or str(product_size.get()) == "" or
                    str(product_value.get()) == "" or product_path.get() == ""):
                onError(error_message)
            else:
                try:
                    add_product()
                    onInfo(message)
                except:
                    onError("Ошибка добавления в базу данных!\n\nПроверьте правильность заполнения полей." +
                            " В частности, название продукта должно быть уникальным.\n\n" +
                            "Для получения информации о текущей БД щёлкните на кнопку \"Показать базу данных\"" +
                            " на главном окне приложения.")

        add.bind('<Button-1>', check_new_product)
        add.pack(pady=20)

    def create_functions_for_lostbox(data_list):
        new = []
        for i in range(len(data_list)):
            for j in range(len(data_list[i])):
                new.append(data_list[i][j])
        return new

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
             text="Введите категорию функциональности продукта",
             font=("Comic Sans MS", 18),
             bg="gray16", fg="white").pack()

    category = create_category_list(connection)
    category = list(set(create_functions_for_lostbox(category)))

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

    # error_message = "Не заполнены необходимые поля!"

    def find(_):
        if product_name.get() == "" or lb.get(ANCHOR) == "" or product_provider.get() == "":
            onError("Не заполнены необходимые поля")
        else:
            try:
                data_list1 = find_local(
                    connection,
                    product_name.get(),
                    lb.get(ANCHOR),
                    product_provider.get(),
                )
                if len(data_list1) == 0:
                    onError("Продукт не найден!\n\nПроверьте правильность заполнения полей." +
                            " В частности, название продукта должно быть уникальным.\n\n" +
                            "Для получения информации о текущей БД щёлкните на кнопку \"Показать базу данных\"" +
                            " на главном окне приложения.")
                    return 0

                data_list2 = find_category(connection, lb.get(ANCHOR))
                return About(app, "Найденный продукт:\n" + to_str(data_list1) + "\n\nАналоги:\n" + to_str(data_list2))
            except:
                onError("Ошибка запроса к БД. Проверьте правильность заполнения полей")

    found.bind('<Button-1>', find)
    found.pack(pady=15)

    add_product = tk.Button(app,
                            text="Добавить продукт",
                            font=("Comic Sans MS", 14, "bold"),
                            bg="lightgreen",
                            width=15, height=1,
                            command=createNewWindow)
    add_product.pack()

    btn_show_table = tk.Button(text="Показать базу данных",
                               font=("Comic Sans MS", 14, "bold"),
                               bg="orchid1",
                               width=20, height=1)

    def create_table(_):
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

        for row in data_list3:
            table.insert('', END, values=row)

        table.pack(expand=YES, fill=BOTH)
        table_frame.pack(expand=YES, fill=BOTH)

    btn_show_table.bind('<Button-1>', create_table)
    btn_show_table.pack(pady=15)

    app.mainloop()
