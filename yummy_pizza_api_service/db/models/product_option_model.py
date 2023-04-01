from enum import Enum

from functools import reduce
import ormar
from typing import Optional

from yummy_pizza_api_service.db.base import BaseModel, BaseMeta
from yummy_pizza_api_service.db.models.product_model import ProductModel


class ProductOptionKind(Enum):
    number_count = "number_count"
    extra_or_reduce = "extra_or_reduce"
    size = "size"


class ProductOptionModel(BaseModel):
    name: str = ormar.String(max_length=200)
    description: str = ormar.String(max_length=500)
    extra_charge: float = ormar.Float()
    option_kind: str = ormar.String(choices=list(ProductOptionKind))
    max_count: int = ormar.Integer(minimum=0)
    min_count: int = ormar.Integer()
    kal: float = ormar.Float()
    option_for_product: Optional[ProductModel] = ormar.ForeignKey(
        ProductModel, related_name="options")
    
    available_options: Optional[str] = ormar.String()

    class Meta(BaseMeta):
        tablename = "production_option"
