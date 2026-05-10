# Программа для работы с данными о криптовалютах (coinmarketcap)

def menu():
    print("\n=== Криптовалюты ===")
    print("1. Загрузить данные из CSV файла")
    print("2. Загрузить данные с сайта coinmarketcap.com")
    print("3. Показать все загруженные данные")
    print("4. Поиск криптовалюты по названию")
    print("0. Выход")
    choice = input("Выберите пункт: ")
    return choice


def main():
    data = []

    while True:
        choice = menu()

        if choice == "1":
            print("(пока не реализовано)")
        elif choice == "2":
            print("(пока не реализовано)")
        elif choice == "3":
            print("(пока не реализовано)")
        elif choice == "4":
            print("(пока не реализовано)")
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
