import tkinter as tk
from tkinter import messagebox as mb, ttk

from library.products import *


def createNewWindow(connection, app):
    def onError(error_message):
        mb.showerror("Ошибка", error_message)

    # создание окна успешного выполнения
    def onInfo(message):
        mb.showinfo("Информация", message)

    newWindow = tk.Toplevel(app)
    newWindow["bg"] = "gray16"
    newWindow.title("Добавление нового продукта")
    newWindow.geometry("600x650+450+50")

    # настройка строк ввода данных для поиска продукта
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

    # метод добавления нового продукта и производителя в базу данных
    def add_product():
        # если при добавлении продукта производитель с таким именем, которое ввел пользователь, не существует,
        # то добавляем производителя в таблицу providers (там ему автоматически присвоится уникальный id)
        if len(get_provider_id(connection, product_provider.get())) == 0:
            add_provider(connection, product_provider.get())
        # получаем id производителя из базы данных по имени производителя (из таблицы providers)
        provider_id = get_provider_id(connection, product_provider.get())
        # добавляем продукт в library
        add_db_row(
            connection,
            product_name.get(),
            product_category.get(),
            provider_id[0][0],
            product_requirements.get(),
            product_size.get(),
            product_value.get(),
            product_path.get(),
        )

    # проверяем правильность заполнения полей для добавления продукта
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