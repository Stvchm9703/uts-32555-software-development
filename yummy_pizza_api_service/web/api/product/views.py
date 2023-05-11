from typing import List

from fastapi import APIRouter, status
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse

from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
from yummy_pizza_api_service.db.models.product_model import Product, ProductType
from yummy_pizza_api_service.web.api.product.schema import (
    ProductModelDTO, ProductModelInputDTO, ProductModelSearchInputDTO
)
from yummy_pizza_api_service.web.api.based import MESSAGE_SETTING, Message

router = APIRouter()


@router.get("/",
            response_model=List[ProductModelDTO],
            responses={**MESSAGE_SETTING}  # type: ignore
            )
async def get_product_models(
    limit: int = 15,
    offset: int = 0,
    product_dao: ProductDAO = Depends(),
):
    """
    Retrieve all product objects from the database.

    :param limit: limit of product objects, defaults to 10.

    :param offset: offset of product objects, defaults to 0.

    :param product_dao: DAO for product models.

    :return: list of product objects from database.
    """
    try:
        return await product_dao.get_all_products(limit=limit, offset=offset)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=Message(status="error", reason=str(e)).dict())


@router.post("/search/",
             response_model=List[ProductModelDTO],
             responses={**MESSAGE_SETTING}  # type: ignore
             )
async def filter_product_models(
    query: ProductModelSearchInputDTO,
    product_dao: ProductDAO = Depends(),
):
    """
    Get all product objects with filter params from the database.

    :params query: query set for searching 

    :return: list of product objects from database.
    """
    try:
        return await product_dao.filter(**query.dict())
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=Message(status="error", reason=str(e)).dict())


@router.post("/create/",
             response_model=ProductModelDTO,
             responses={**MESSAGE_SETTING}  # type: ignore
             )
async def create_product_model(
    new_product_object: ProductModelInputDTO,
    product_dao: ProductDAO = Depends(),
):
    """
    Creates Product model in the database.

    :param new_product_object: new product model item. 
    :param product_dao: DAO for product models.

    :return `edited`: new created object
    :return `status` : status 
    """
    try:
        await product_dao.create(product=new_product_object.dict())
        created = await product_dao.filter(keyword=new_product_object.name, prod_type=new_product_object.item_type)
        return created[0]
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=Message(status="error", reason=str(e)).dict())


@router.post("/update/",
             response_model=Message,
             responses={**MESSAGE_SETTING}
             )
async def update_product_model(
    product_object: ProductModelInputDTO,
    product_dao: ProductDAO = Depends(),
):
    """
    Update Product model in the database.

    :param product_object: the product model item that need to be update,(id is necessary).
    :param product_dao: DAO for product models.

    :return `edited`: updated object
    :return `status`: status
    """
    try:
        updated = await product_dao.update(product=product_object)  # type: ignore
        return Message(
            edited=updated,
            status="complete"
        )  # type: ignore
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=Message(status="error", reason=str(e)).dict())


@router.post("/delete/",
             response_model=Message,
             responses={**MESSAGE_SETTING}
             )
async def delete_product_model(
    product_object: ProductModelInputDTO,
    product_dao: ProductDAO = Depends(),
):
    """
    Delete Product model within the database.

    :param product_object: the target product model item that need to be delete,(id is necessary).
    :param product_dao: DAO for product models.

    :return `edited`: deleted object
    :return `status`: status
    """
    try:
        deleted = await product_dao.delete(product=Product(**product_object.dict()))
        return Message(
            edited=deleted,
            status="complete"
        )  # type: ignore
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=Message(status="error", reason=str(e)).dict())
