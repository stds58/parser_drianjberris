import asyncio
from app.services.item import add_many_item
from app.utils.wildberies_parser import WildBeriesParser

async def run_parser(phrase: str, search_id: int, session):
    parser = WildBeriesParser(phrase)
    async for product in parser.get_products_stream():
        product["search_id"] = search_id
        await add_many_item(product, session)

