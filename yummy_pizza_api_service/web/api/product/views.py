from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
from yummy_pizza_api_service.db.models.product_model import Product, ProductType
from yummy_pizza_api_service.web.api.product.schema import (
    ProductModelDTO, ProductModelInputDTO, ProductModelSearchInputDTO
)

router = APIRouter()


@router.get("/", response_model=List[ProductModelDTO])
async def get_product_models(
    limit: int = 15,
    offset: int = 0,
    product_dao: ProductDAO = Depends(),
) -> List[Product]:
    """
    Retrieve all product objects from the database.

    :param limit: limit of product objects, defaults to 10.

    :param offset: offset of product objects, defaults to 0.

    :param product_dao: DAO for product models.

    :return: list of product objects from database.
    """
    return await product_dao.get_all_products(limit=limit, offset=offset)


@router.post("/search/", response_model=List[ProductModelDTO])
async def filter_product_models(
    query: ProductModelSearchInputDTO,
    product_dao: ProductDAO = Depends(),
) -> List[Product]:
    """
    Get all product objects with filter params from the database.

    :params query: query set for searching 

    :return: list of product objects from database.
    """
    return await product_dao.filter(**query)


@router.post("/create/")
async def create_product_model(
    new_product_object: ProductModelInputDTO,
    product_dao: ProductDAO = Depends(),
) -> Product:
    """
    Creates Product model in the database.

    :param new_product_object: new product model item. 
    :param product_dao: DAO for product models.

    :return `edited`: new created object
    :return `status` : status 
    """
    await product_dao.create(product=new_product_object.dict())
    created = await product_dao.filter(keyword=new_product_object.name, prod_type=ProductType[new_product_object.item_type])
    return created[0]


@router.post("/update/")
async def update_product_model(
    product_object: ProductModelInputDTO,
    product_dao: ProductDAO = Depends(),
) -> dict:
    """
    Update Product model in the database.

    :param product_object: the product model item that need to be update,(id is necessary).
    :param product_dao: DAO for product models.

    :return `edited`: updated object
    :return `status`: status
    """
    updated = await product_dao.update(product=product_object) # type: ignore
    return {
        "edited": updated,
        "status": "complete"
    }


@router.post("/delete/")
async def delete_product_model(
    product_object: ProductModelInputDTO,
    product_dao: ProductDAO = Depends(),
) -> dict:
    """
    Delete Product model within the database.

    :param product_object: the target product model item that need to be delete,(id is necessary).
    :param product_dao: DAO for product models.

    :return `edited`: deleted object
    :return `status`: status
    """
    deleted = await product_dao.delete(product=product_object)
    return {
        "edited": deleted,
        "status": "complete"
    }
