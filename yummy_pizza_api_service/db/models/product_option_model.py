from enum import Enum

from functools import reduce
import ormar
from typing import Optional, List

from yummy_pizza_api_service.db.base import BaseModel, BaseMeta
from yummy_pizza_api_service.db.models.product_model import Product


class ProductOptionKind(Enum):
    number_count = "number_count"
    extra_or_reduce = "extra_or_reduce"
    size = "size"
    favour = "favour"


class ProductOption(BaseModel):
    __table_args__ = {'extend_existing': True}

    name: str = ormar.String(max_length=200)
    description: str = ormar.String(max_length=500)
    extra_charge: float = ormar.Float()
    option_kind: str = ormar.String(max_length=200, choices=list(ProductOptionKind))
    max_count: Optional[int] = ormar.Integer(minimum=0, nullable=True)
    min_count: Optional[int] = ormar.Integer(nullable=True)
    kal: Optional[float] = ormar.Float(nullable=True)
    _option_sets: Optional[str] = ormar.String(max_length=500, nullable=True)
    option_for_product: Optional[Product] = ormar.ForeignKey(
        Product,
        related_name="options",
        name="fk_options_product"
    )

    @property
    def option_sets(self) -> List[str]:
        return self._option_sets.split(',') or []

    @option_sets.setter
    def option_sets(self, val: List[str]):
        self._option_sets = ','.join(val)

   
    class Meta(BaseMeta):
        tablename = "production_option"
