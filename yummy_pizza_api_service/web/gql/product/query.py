from typing import List

import strawberry

from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
# from yummy_pizza_api_service.web.api.product.schema import ProductModelDTO
from yummy_pizza_api_service.web.gql.product.schema import ProductDTO


@strawberry.type
class Query:
    """Query to interact with dummies."""

    @strawberry.field(description="Get all dummies")
    async def get_product_models(
        self,
        limit: int = 15,
        offset: int = 0,
        product_query: ProductDTO = None
    ) -> List[ProductDTO]:
        """
        Retrieves all dummy objects from database.

        :param limit: limit of dummy objects, defaults to 10.
        :param offset: offset of dummy objects, defaults to 0.
        :return: list of dummy obbjects from database.
        """
        dao = ProductDAO()
        return await dao.filter(**product_query, limit=limit, offset=offset)  # type: ignore
