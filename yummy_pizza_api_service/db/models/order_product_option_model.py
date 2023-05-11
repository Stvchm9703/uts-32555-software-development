
from typing import List, Optional
from functools import reduce
import ormar
from yummy_pizza_api_service.db.base import BaseMeta, BaseModel
from yummy_pizza_api_service.db.models.product_model import Product
from yummy_pizza_api_service.db.models.product_option_model import ProductOption

from yummy_pizza_api_service.db.models.order_product_model import OrderProduct


class OrderProductOption(BaseModel):
    __table_args__ = {'extend_existing': True}

    option: str = ormar.String(max_length=500, nullable=True)
    count: int = ormar.Integer(nullable=True)
    charge: float = ormar.Float(nullable=True)
    option_referance: Optional[ProductOption] = ormar.ForeignKey(
        ProductOption,
        related_name="options",
        name="fk_options_product",
        skip_reverse=True,
        nullable=False
    )
    order_option_for: Optional[OrderProduct] = ormar.ForeignKey(
        ProductOption,
        related_name="extra_options",
        name="fk_order_product",
        nullable=False
        # skip_reverse=True,
    )

    class Meta(BaseMeta):
        tablename = "ordprodopt"
