from app.services.item import add_many_item
#from app.services.search import update_one_search
from app.utils.wildberies_parser import WildBeriesParser
from sqlalchemy.ext.asyncio import AsyncSession


async def run_parser(phrase_id: int, phrase: str, session: AsyncSession):
    page = 1
    while True:
        if page == 5:
            break
        parser = WildBeriesParser(phrase, page)
        if parser is None:
            break
        products = await  parser.get_response
        for product in products:
            product['id_search'] = phrase_id
        await add_many_item(session=session, data=products)
        page += 1
        yield products
    #result = update_one_search(phrase_id=phrase_id, session=session)
    yield "ok"






