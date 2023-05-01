from typing import List

from fastapi import APIRouter, status, HTTPException
from fastapi.param_functions import Depends

# from redis.asyncio import Redis

# from yummy_pizza_api_service.services.redis.models.order_model import Order
# from yummy_pizza_api_service.services.redis.models.order_product_model import

# from yummy_pizza_api_service.services.redis.dependency import get_redis_pool


from yummy_pizza_api_service.db.dao.order_dao import OrderDAO
from yummy_pizza_api_service.db.models.product_model import Product
from yummy_pizza_api_service.db.models.order_model import Order

from yummy_pizza_api_service.web.api.order.schema import (
    OrderInputDTO,
    OrderDTO,
    OrderRefProductDTO,
)

router = APIRouter()


@router.get("/list_order", response_model=List[OrderDTO])
async def get_orders(
    limit: int = 15,
    offset: int = 0,
    order_dao: OrderDAO = Depends()
) -> List[Order]:
    return await order_dao.get_latest_order(limit=limit, offset=offset)


@router.post("/create_order", response_class=OrderDTO)
async def create_order(
    new_order: OrderInputDTO,
    order_dao: OrderDAO = Depends()
) -> Order:
    await order_dao.create(order=new_order.dict())
    created = await order_dao.filter(keyword=new_order.name, prod_type=ProductType[new_product_object.item_type])
    return {
        "edited": created,
        "status": "complete"
    }


@router.post("/search", response_class=OrderDTO)
async def filter_order_models(
    order_filter_query: OrderInputDTO,
    order_dao: OrderDAO = Depends()
) -> List[Order]:

    return await order_dao.filter(**order_filter_query.dict())


@router.post("/add_item")
async def add_item(
    updated_order: OrderRefProductDTO,
    order_dao: OrderDAO = Depends()
) -> Order:

    if updated_order.id == None or updated_order.order_number == None:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail={
                "edited": None,
                "reason": "request order is empty id",
                "status": "PRECONDITION_FAILED"
            }
        )

    if updated_order.product == None:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail={
                "edited": None,
                "reason": "empty items",
                "status": "PRECONDITION_FAILED"
            }
        )

    existed = []
    if updated_order.id != None:
        existed = await order_dao.filter( query={'id': updated_order.id} )
    elif updated_order.order_number != None:
        existed = await order_dao.filter(query={'order_number': updated_order.order_number})

    if len(existed) != 1:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail={
                "edited": None,
                "reason": "request order is not single one",
                "status": "PRECONDITION_FAILED"
            }
        )
    
    existed = existed[0]
    try :
        for opt in updated_order.items:
            await order_dao.add_item(existed, opt)
    except:
        raise HTTPException(
            status_code=status.HTTP,
            detail={
                "edited": None,
                "reason": "request order is not single one",
                "status": "PRECONDITION_FAILED"
            }
        )
    return {
        "edited": existed[0].dict(),
        "status": "complete"
    }


@router.post("/remove_item", response_class=OrderDTO)
async def remove_item() -> Order:
    return


@router.post("/cancel_order", response_class=OrderDTO)
async def cancel_order() -> Order:
    return


@router.post("/complete_order", response_class=OrderDTO)
async def complete_order() -> Order:
    return


@router.post("/get_recept")
async def get_recept() -> str:
    return
