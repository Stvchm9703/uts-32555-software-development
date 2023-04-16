from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from redis.asyncio import Redis

from yummy_pizza_api_service.services.redis.models.order_model import Order
# from yummy_pizza_api_service.services.redis.models.order_product_model import

from yummy_pizza_api_service.services.redis.dependency import get_redis_pool


from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
from yummy_pizza_api_service.db.models.product_model import Product
from yummy_pizza_api_service.web.api.order.schema import (
    OrderInputDTO,
    OrderDTO
)

router = APIRouter()


@router.get("/list/", response_model=List[OrderDTO])
async def get_orders(
    limit: int = 15,
    offset: int = 0,
    redis_service: Redis = Depends(get_redis_pool)
) -> List[Order]:

    # return await product_dao.get_all_products(limit=limit, offset=offset)
    rww = await redis_service.keys("order")
    
    return []

@router.get("/{order_number}", response_class=OrderDTO)
async def get_order() -> Order:
    return





@router.get("/create", response_class=OrderDTO)
async def create_order() -> Order:
    return
