from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
from yummy_pizza_api_service.db.models.product_model import Product
from yummy_pizza_api_service.web.api.product.schema import (
    ProductModelDTO, ProductModelInputDTO
)

router = APIRouter()


@router.get("/", response_model=List[ProductModelDTO])
async def get_product_models(
    limit: int = 15,
    offset: int = 0,
    product_dao: ProductDAO = Depends(),
) -> List[Product]:
    """
    Retrieve all dummy objects from the database.

    :param limit: limit of dummy objects, defaults to 10.
    :param offset: offset of dummy objects, defaults to 0.
    :param dummy_dao: DAO for dummy models.
    :return: list of dummy obbjects from database.
    """
    return await product_dao.get_all_products(limit=limit, offset=offset)


@router.post("/create/")
async def create_product_model(
    new_product_object: ProductModelInputDTO,
    product_dao: ProductDAO = Depends(),
) -> List[Product]:
    """
    Creates dummy model in the database.

    :param new_dummy_object: new dummy model item.
    :param dummy_dao: DAO for dummy models.
    """
    await product_dao.create(product=new_product_object.dict())

    return await product_dao.filter(keyword=new_product_object.name)


@router.post("/update/")
async def update_product_model(
    product_object: ProductModelInputDTO,
    product_dao: ProductDAO = Depends(),
) -> dict:
    updated = await product_dao.update(product=product_object)
    return {
        "edited": updated,
        "status": "complete"
    }


@router.post("/delete/")
async def delete_product_model(
    product_object: ProductModelInputDTO,
    product_dao: ProductDAO = Depends(),
) -> dict:
    deleted = await product_dao.delete(product=product_object)
    return {
        "edited": deleted,
        "status": "complete"
    }
