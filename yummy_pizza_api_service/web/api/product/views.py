from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
from yummy_pizza_api_service.db.models.product_model import ProductModel
from yummy_pizza_api_service.web.api.product.schema import (
    ProductModelDTO, ProductModelInputDTO
)

router = APIRouter()


@router.get("/", response_model=List[ProductModelDTO])
async def get_product_models(
    limit: int = 15,
    offset: int = 0,
    product_dao: ProductDAO = Depends(),
) -> List[ProductModel]:
    """
    Retrieve all dummy objects from the database.

    :param limit: limit of dummy objects, defaults to 10.
    :param offset: offset of dummy objects, defaults to 0.
    :param dummy_dao: DAO for dummy models.
    :return: list of dummy obbjects from database.
    """
    return await product_dao.get_all_products(limit=limit, offset=offset)


# @router.put("/")
# async def create_dummy_model(
#     new_dummy_object: DummyModelInputDTO,
#     dummy_dao: DummyDAO = Depends(),
# ) -> None:
#     """
#     Creates dummy model in the database.

#     :param new_dummy_object: new dummy model item.
#     :param dummy_dao: DAO for dummy models.
#     """
#     await dummy_dao.create_dummy_model(**new_dummy_object.dict())
