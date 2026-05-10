# Программа для работы с данными о криптовалютах (coinmarketcap)

import csv


def menu():
    print("\n=== Криптовалюты ===")
    print("1. Загрузить данные из CSV файла")
    print("2. Загрузить данные с сайта coinmarketcap.com")
    print("3. Показать все загруженные данные")
    print("4. Поиск криптовалюты по названию")
    print("0. Выход")
    choice = input("Выберите пункт: ")
    return choice


# Чтение данных из csv файла
def load_from_csv(filename):
    data = []
    try:
        file = open(filename, encoding="utf-8")
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return data

    reader = csv.reader(file)
    next(reader)  # пропускаем заголовок

    for row in reader:
        # в csv числа записаны с запятой вместо точки, заменяем
        coin = {
            "id": int(row[0]),
            "name": row[1],
            "symbol": row[2],
            "slug": row[3],
            "circulating_supply": float(row[4].replace(",", ".")),
            "price": float(row[5].replace(",", ".")),
            "market_cap": float(row[6].replace(",", "."))
        }
        data.append(coin)

    file.close()
    print(f"Загружено {len(data)} криптовалют из файла.")
    return data


def main():
    data = []

    while True:
        choice = menu()

        if choice == "1":
            data = load_from_csv("currencies26.csv")
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
