import requests
from typing import Optional, Dict, List


class WildBeriesParser:
    def __init__(self, words):
        self.words = words

    def create_response(self, page: int) -> Optional[Dict]:
        url_api = (f"https://search.wb.ru/exactmatch/ru/common/v4/search"
                   f"?appType=1&curr=rub&dest=-1257786&page={page}&query='%20{self.words}&"
                   f"resultset=catalog&sort=popular&spp=24&suppressSpellcheck=false"
                   )
        headers = {'Accept': "*/*", 'User-Agent': "Chrome/51.0.2704.103 Safari/537.36"}
        response = requests.get(url_api, headers=headers)
        if response.status_code == 200:
            result = response.json()
        else:
            result = None
        return result

    def parse_response(self, data: Dict) -> Optional[List[Dict]]:
        products = data.get('data', {}).get('products', [])
        count_items = 0
        list_items= []
        for product in products:
            row = {}
            row['name'] = product.get('name')
            row['brand'] = product.get('brand')
            row['price_u'] = product.get('priceU')
            row['sale_price_u'] = product.get('salePriceU')
            row['feedbacks'] = product.get('feedbacks')
            row['rating'] = product.get('rating')
            list_items.append(row)
            count_items += 1
        if count_items == 0:
            result = None
        else:
            result = list_items
        return result

    @property
    def get_response(self) -> Optional[List[Dict]]:
        page = 1
        lists = []
        while True:
            # if page == 5:
            #     break
            data = self.create_response(page)
            if data is None:
                break
            result = self.parse_response(data)
            if result is None:
                break
            lists.append(result)
            page += 1
        rows = [x for sublist in lists for x in sublist]
        return rows

if __name__ == "__main__":
    tovar = "зонт мужской антиветер"
    result = WildBeriesParser(tovar)
    print(result.words)
    print(result.get_response)

# page = 1
# tovar = "зонт % 20мужской % 20антиветер"
#
# url_api = (f"https://search.wb.ru/exactmatch/ru/common/v4/search"
#                    f"?appType=1&curr=rub&dest=-1257786&page={page}&query='%20{tovar}&"
#                    f"resultset=catalog&sort=popular&spp=24&suppressSpellcheck=false"
#                    )
# headers = {'Accept': "*/*", 'User-Agent': "Chrome/51.0.2704.103 Safari/537.36"}
# response = requests.get(url_api, headers=headers)
# data = response.json()
#
# if response.status_code == 200:
#     data = response.json()
#     #print(data)
#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#     else:
#         print("Ошибка:", response.status_code)
#         print("Ответ:", response.text)
# else:
#     print("Ошибка:", response.status_code)
#     print("Ответ:", response.text)
#
#
# # Проверим структуру данных
# products = data.get('data', {}).get('products', [])
# i=0
# # Пройдемся по каждому товару и выведем информацию
# for product in products:
#     name = product.get('name')
#     brand = product.get('brand')
#     price_u = product.get('priceU')  # цена в копейках
#     sale_price_u = product.get('salePriceU')  # цена со скидкой в копейках
#     feedbacks = product.get('feedbacks')  # количество отзывов
#     rating = product.get('rating')  # рейтинг
#
#     if sale_price_u / 100 <= 450:
#         print(f"Наименование: {name}")
#         print(f"Бренд: {brand}")
#         print(f"Цена: {price_u / 100} руб.")
#         print(f"Цена со скидкой: {sale_price_u / 100} руб.")
#         print(f"Отзывы: {feedbacks}")
#         print(f"Рейтинг: {rating}\n")
#
#         i+=1
#
# print(i)


