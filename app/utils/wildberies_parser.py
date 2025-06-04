import aiohttp
from typing import Optional, Dict, List
import json


class WildBeriesParser:
    def __init__(self, words, page):
        self.words = words
        self.page = page

    async def create_response(self, page: int) -> Optional[Dict]:
        url_api = (f"https://search.wb.ru/exactmatch/ru/common/v4/search"
                   f"?appType=1&curr=rub&dest=-1257786&page={page}&query='%20{self.words}&"
                   f"resultset=catalog&sort=popular&spp=24&suppressSpellcheck=false"
                   )
        headers = {'Accept': "*/*", 'User-Agent': "Chrome/51.0.2704.103 Safari/537.36"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url_api, headers=headers) as response:
                if response.status != 200:
                    return None

                content_type = response.headers.get('Content-Type', '')
                text = await response.text()
                try:
                    # Пытаемся распарсить как JSON
                    return json.loads(text)
                except json.JSONDecodeError:
                    print("Failed to decode JSON. Raw response:")
                    print(text[:500])  # Выводим начало для диагностики
                    return None

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
            row['wb_id'] = product.get('id')
            list_items.append(row)
            count_items += 1
        if count_items == 0:
            result = None
        else:
            result = list_items
        return result

    @property
    async def get_response(self) -> Optional[List[Dict]]:
        response = await self.create_response(self.page)
        return self.parse_response(response)

if __name__ == "__main__":
    import asyncio
    tovar = "зонт мужской антиветер"
    async def main():
        parser = WildBeriesParser(tovar, page=1)
        result = await parser.get_response
        print(result)

    asyncio.run(main())

