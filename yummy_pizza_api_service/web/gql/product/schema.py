import strawberry
from typing import List, Optional
from yummy_pizza_api_service.web.api.product.schema import ProductModelDTO, ProductModelInputDTO, ProductOptionModelDTO


@strawberry.type
class ProductOptionDTO:
    id: int
    name: str
    description: str
    extra_charge: float
    option_kind: str
    max_count: int
    min_count: int
    kal: float
    option_sets: List[str]


@strawberry.type
class ProductDTO:
    # refer to ProductModelDTO
    """
    DTO for Product models.

    It returned when accessing dummy models from the API.
    """
    id: Optional[ int]
    name:  str
    description: str
    item_type: str
    category: str
    kal: Optional[float]
    price_value: Optional[float]
    rate: Optional[float]
    options: List[ProductOptionDTO]
