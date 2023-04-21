import strawberry
from typing import Optional, List
from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
# from yummy_pizza_api_service.web.api.product.schema import ProductModelInputDTO, ProductModelDTO
from yummy_pizza_api_service.web.gql.product.schema import ProductDTO


@strawberry.input
class ProductInputDTO:
    """ ProductInputDTO """
    limit: Optional[int]
    offset: Optional[int]
    previous: Optional[str]
    next: Optional[str]
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    item_type: Optional[str]
    category: Optional[str]
    price_max_range: Optional[float]
    price_min_range: Optional[float]

@strawberry.type
class Mutation:
    """Mutations for product."""
    @strawberry.field(description="Get all product")
    async def get_product_models(
        self,
        search_input: ProductInputDTO
    ) -> List[ProductDTO]:
        """
        Retrieves all dummy objects from database.

        :param limit: limit of dummy objects, defaults to 10.
        :param offset: offset of dummy objects, defaults to 0.
        :return: list of dummy obbjects from database.
        """
        dao = ProductDAO()
        # type: ignore
        result = await dao.filter(**search_input)
        return result
