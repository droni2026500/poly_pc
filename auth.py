# Импорт классов
from classes import *
from registrator import *


def log(enter_login, enter_password, root, main_reg):
    auth = Auth(enter_login.get(), enter_password.get(), root, main_reg)
    auth.log_pas()


def main():
    # Окно авторизации
    root = Tk()  # Создание окна
    root.geometry("300x250")  # Размер окна
    root.title("Войти в систему")  # Название окна
    root.config(background="#fff44f")  # Фон формы
    root.resizable(
        width=False, height=False
    )  # Настройка,чтобы нельзя было изменять размер окна
    text_log = Label(
        text="Вход в систему", background="#fff44f", font="times 12"
    )  # Лейбл 'ход в систему'
    text_enter_login = Label(
        text="Введите ваш логин:", background="#fff44f", font="times 12"
    )  # Лейбл введите логин
    enter_login = Entry()  # Поле ввода логина
    text_enter_pass = Label(
        text="Введите ваш пароль:", background="#fff44f", font="times 12"
    )  # Лейбл "Введите ваш пароль"
    enter_password = Entry(show="*")  # Поле ввода пароля
    button_enter = Button(
        text="Войти",
        command=lambda: log(enter_login, enter_password, root, main_reg),
        background="#71bc78",
        foreground="white",
        font="times 12",
    )  # Кнопка входа
    # Расположение элементов на форме
    text_log.pack()
    text_enter_login.pack()
    enter_login.pack()
    text_enter_pass.pack()
    enter_password.pack()
    button_enter.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
