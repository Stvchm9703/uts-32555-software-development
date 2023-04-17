from typing import List, Optional
from functools import reduce
import ormar
from yummy_pizza_api_service.db.base import BaseMeta, BaseModel
from yummy_pizza_api_service.db.models.product_model import Product
from yummy_pizza_api_service.db.models.product_option_model import ProductOption
from yummy_pizza_api_service.db.models.order_model import Order


class OrderProduct(BaseModel):
    __table_args__ = {'extend_existing': True}
    base_referance: Optional[Product] = ormar.ForeignKey(
        Product,
        name="fk_base_referance_product",
        skip_reverse=True,
        nullable=False
    )
    remark: str
    for_order: Optional[Order] = ormar.ForeignKey(
        Order,
        name="fk_order_refer"
    )

    class Meta(BaseMeta):
        tablename = "ordprod"
