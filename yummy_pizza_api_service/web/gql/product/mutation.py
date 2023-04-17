import strawberry

from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
# from yummy_pizza_api_service.web.api.product.schema import ProductModelInputDTO, ProductModelDTO
from yummy_pizza_api_service.web.gql.product.schema import ProductDTO
@strawberry.type
class Mutation:
    """Mutations for product."""

    # @strawberry.mutation(description="Create Pr object in a database")
    # async def create_dummy_model(
    #     self,
    #     name: str,
    # ) -> str:
    #     """
    #     Creates dummy model in a database.

    #     :param name: name of a dummy.
    #     :return: name of a dummt model.
    #     """
    #     dao = DummyDAO()
    #     await dao.create_dummy_model(name=name)
    #     return name

    # @strawberry.mutation(description="Create product in a database")
    # async def create_product_model(
    #     self, 
    #     input: ProductDTO,
    # ) -> ProductDTO:
    #     dao = ProductDAO()
    #     return await dao.create(**(input.dict()))
