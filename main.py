# Программа для работы с данными о криптовалютах (coinmarketcap)

import csv
import requests
from bs4 import BeautifulSoup


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


# Убираем символ $ и запятые из строки с ценой, возвращаем число
def parse_price(text):
    text = text.replace("$", "").replace(",", "")
    return float(text)


# Парсим market_cap — берём полное значение из второго span
def parse_market_cap(td):
    spans = td.find_all("span")
    if len(spans) >= 2:
        return parse_price(spans[1].get_text(strip=True))
    return 0.0


# Парсим circulating_supply — текст вида "20.02MBTC"
def parse_supply(td):
    div = td.find("div", class_="circulating-supply-value")
    if not div:
        return 0.0
    span = div.find("span")
    if not span:
        return 0.0
    text = span.get_text(strip=True)

    # суффиксы: K=тысячи, M=миллионы, B=миллиарды, T=триллионы
    multipliers = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000, "T": 1_000_000_000_000}
    for suffix, mult in multipliers.items():
        if text.endswith(suffix):
            return float(text[:-1]) * mult
    return float(text)


# Загрузка данных с сайта coinmarketcap.com через requests + BeautifulSoup
def load_from_site(count=10):
    url = "https://coinmarketcap.com/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    print("Загружаю страницу coinmarketcap.com...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        print("Не удалось найти таблицу на странице!")
        return []

    rows = table.find_all("tr")
    data = []

    # первые две строки — заголовок и индекс, пропускаем
    for row in rows[2:]:
        cells = row.find_all("td")
        if len(cells) < 10:
            continue

        # td[2] — название и символ (в двух тегах <p>)
        td_name = cells[2]
        link = td_name.find("a")
        href = link.get("href", "") if link else ""
        slug = href.replace("/currencies/", "").strip("/")

        img = td_name.find("img")
        img_src = img.get("src", "") if img else ""
        coin_id = img_src.split("/")[-1].replace(".gif", "").replace(".png", "")

        ps = td_name.find_all("p")
        name = ps[0].get_text(strip=True) if len(ps) > 0 else ""
        symbol = ps[1].get_text(strip=True) if len(ps) > 1 else ""

        # td[3] — цена, td[7] — market cap, td[9] — circulating supply
        price = parse_price(cells[3].get_text(strip=True))
        market_cap = parse_market_cap(cells[7])
        supply = parse_supply(cells[9])

        coin = {
            "id": int(coin_id) if coin_id.isdigit() else 0,
            "name": name,
            "symbol": symbol,
            "slug": slug,
            "circulating_supply": supply,
            "price": price,
            "market_cap": market_cap
        }
        data.append(coin)

        if len(data) >= count:
            break

    print(f"Загружено {len(data)} криптовалют с сайта.")
    return data


# Поиск криптовалюты по названию (частичное совпадение)
def search_by_name(data, query):
    query = query.lower()
    results = []
    for coin in data:
        if query in coin["name"].lower():
            results.append(coin)
    return results


# Вывод информации об одной криптовалюте
def print_coin(coin):
    print(f"  ID:           {coin['id']}")
    print(f"  Название:     {coin['name']}")
    print(f"  Символ:       {coin['symbol']}")
    print(f"  Slug:         {coin['slug']}")
    print(f"  В обращении:  {coin['circulating_supply']:.2f}")
    print(f"  Цена (USD):   {coin['price']:.2f}")
    print(f"  Капитализация:{coin['market_cap']:.2f}")


def main():
    data = []

    while True:
        choice = menu()

        if choice == "1":
            data = load_from_csv("currencies26.csv")
        elif choice == "2":
            data = load_from_site(10)
        elif choice == "3":
            if not data:
                print("Данные не загружены! Сначала выберите пункт 1 или 2.")
            else:
                print(f"\nВсего загружено: {len(data)} криптовалют\n")
                for coin in data:
                    print(f"--- {coin['name']} ({coin['symbol']}) ---")
                    print_coin(coin)
                    print()
        elif choice == "4":
            if not data:
                print("Данные не загружены! Сначала выберите пункт 1 или 2.")
            else:
                query = input("Введите название криптовалюты: ")
                results = search_by_name(data, query)
                if results:
                    print(f"\nНайдено: {len(results)}\n")
                    for coin in results:
                        print(f"--- {coin['name']} ({coin['symbol']}) ---")
                        print_coin(coin)
                        print()
                else:
                    print("Ничего не найдено.")
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
