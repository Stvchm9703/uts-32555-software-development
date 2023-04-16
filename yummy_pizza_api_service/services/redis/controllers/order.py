from typing import List, Any
import json
import pydash
from hashids import Hashids
from datetime import datetime
from redis.asyncio import Redis

from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
# from yummy_pizza_api_service.db.dao.order_dao import
from yummy_pizza_api_service.services.redis.models.order_model import Order
from yummy_pizza_api_service.services.redis.models.order_product_model import OrderProduct
from yummy_pizza_api_service.web.api.order.schema import (
    OrderInputDTO,
    OrderDTO,
    OrderProductDTO
)
from yummy_pizza_api_service.utils.merge import merge_model


RUNTIME_HASH = Hashids('general_order', 6)


async def get_order_list(redis_service: Redis, limit: int, offset: int, OrderQuery: OrderInputDTO) -> List[Order]:
    keylist = await redis_service.keys('order_*')
    if keylist == []:
        return []
    result = await redis_service.mget(keys=keylist[offset:offset + limit])
    result_list = [Order.construct(**(json.loads(result_set))) for result_set in result]

    return pydash.filter_(result_list, OrderQuery.dict(exclude_defaults=True, exclude_none=True, exclude_unset=True))


async def get_order_by_id(redis_service: Redis, id: Any) -> Order:
    result = await redis_service.get('order_{}'.format(id))
    if result == None:
        return None
    return Order.construct(**(json.loads(result)))


async def set_order(redis_service: Redis, order_set: Order) -> Order:
    await redis_service.set('order_{id}'.format(id=order_set.id), order_set.json())
    return await get_order_by_id(order_set.id)


async def clear_order(redis_service: Redis, order_set: Order) -> Order:
    await redis_service.delete('order_{id}'.format(id=order_set.id))
    return None


async def check_order_item(redis_service: Redis, dao: ProductDAO, order_prod: OrderProductDTO) -> bool:
    if order_prod == None:
        return False
    if order_prod.product == None:
        return False
    if order_prod.product.id == None or order_prod.product.id == 0:
        return False
    exist_prod = await dao.get(id=order_prod.product.id)

    return exist_prod != None
    pass


async def create_order(redis_service: Redis, order_input: OrderInputDTO) -> Order:
    new_order = Order(**{
        **(order_input.dict()),
        'id': RUNTIME_HASH.encode(int(datetime.now().timestamp()))
    })
    return await set_order(redis_service, new_order)


async def update_order(redis_service: Redis, order_input: OrderInputDTO) -> Order:
    if order_input.id == "" or order_input.id == None:
        raise "requested_order_has_no_id"
    existed: Order = await get_order_by_id(redis_service, order_input.id)
    if existed == None:
        raise "order_is_not_exist"

    existed = merge_model(existed, order_input, ['id', 'items'])
    return await set_order(redis_service, existed)


async def add_item(redis_service: Redis, order_input: OrderInputDTO , order_item: OrderProductDTO) -> Order:
    if order_input.id == "" or order_input.id == None:
        raise "requested_order_has_no_id"
    existed: Order = await get_order_by_id(redis_service, order_input.id)
    if existed == None:
        raise "order_is_not_exist"
    if existed.update_item(order_item) == False:
        existed.add_item(order_item)
    return await set_order(redis_service, existed)


async def remove_item(redis_service: Redis, order_input: OrderInputDTO, order_item: OrderProductDTO) -> Order:
    if order_input.id == "" or order_input.id == None:
        raise "requested_order_has_no_id"
    existed: Order = await get_order_by_id(redis_service, order_input.id)
    if existed == None:
        raise "order_is_not_exist"
    existed.remove_item(order_item)
    return await set_order(redis_service, existed)
