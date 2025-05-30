import requests
from typing import Optional, Dict, List


class WildBeriesParser:
    def __init__(self, words, page):
        self.words = words
        self.page = page

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
        response = self.create_response(self.page)
        data = self.parse_response(response)
        return data

if __name__ == "__main__":
    tovar = "зонт мужской антиветер"
    result = WildBeriesParser(tovar)
    # print(result.words)
    # print(result.get_response)
