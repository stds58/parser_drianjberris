import requests


page = 1
tovar = "зонт % 20мужской % 20антиветер"

url_api = (f"https://search.wb.ru/exactmatch/ru/common/v4/search"
                   f"?appType=1&curr=rub&dest=-1257786&page={page}&query='%20{tovar}&"
                   f"resultset=catalog&sort=popular&spp=24&suppressSpellcheck=false"
                   )
headers = {'Accept': "*/*", 'User-Agent': "Chrome/51.0.2704.103 Safari/537.36"}
response = requests.get(url_api, headers=headers)
data = response.json()

if response.status_code == 200:
    data = response.json()
    #print(data)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Ошибка:", response.status_code)
        print("Ответ:", response.text)
else:
    print("Ошибка:", response.status_code)
    print("Ответ:", response.text)


# Проверим структуру данных
products = data.get('data', {}).get('products', [])
i=0
# Пройдемся по каждому товару и выведем информацию
for product in products:
    name = product.get('name')
    brand = product.get('brand')
    price_u = product.get('priceU')  # цена в копейках
    sale_price_u = product.get('salePriceU')  # цена со скидкой в копейках
    feedbacks = product.get('feedbacks')  # количество отзывов
    rating = product.get('rating')  # рейтинг

    if sale_price_u / 100 <= 450:
        print(f"Наименование: {name}")
        print(f"Бренд: {brand}")
        print(f"Цена: {price_u / 100} руб.")
        print(f"Цена со скидкой: {sale_price_u / 100} руб.")
        print(f"Отзывы: {feedbacks}")
        print(f"Рейтинг: {rating}\n")

        i+=1

print(i)


