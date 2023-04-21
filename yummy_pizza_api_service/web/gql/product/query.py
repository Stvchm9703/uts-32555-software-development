from typing import List

import strawberry

from yummy_pizza_api_service.db.models.product_model import Product
from yummy_pizza_api_service.db.dao.product_dao import ProductDAO
# from yummy_pizza_api_service.web.api.product.schema import ProductModelDTO
from yummy_pizza_api_service.web.gql.product.schema import ProductDTO


@strawberry.type
class Query:
    """Query to interact with dummies."""


        
