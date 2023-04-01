"""
from typing import List, Optional
from functools import reduce
import ormar
from yummy_pizza_api_service.db.base import BaseMeta, BaseModel
from yummy_pizza_api_service.db.models.product_model import Product
from yummy_pizza_api_service.db.models.product_option_model import ProductOption


class OrderProduct(BaseModel):
    __table_args__ = {'extend_existing': True}

    quality: int = ormar.Integer()
    base_referance: Optional[Product] = ormar.ForeignKey(
        Product,
        name="fk_base_referance_product",
        skip_reverse=True,
        nullable=False
    )
   
    remark: str

    class Meta(BaseMeta):
        tablename = "order_product"

    def total_charge(self) -> float:
        # await self.fetch_related()

        total_extra_charge = [x.extra_charge for x in self.extra_options]

        return float(
            self.base_referance.price_value
            + reduce((lambda x, y: x + y), total_extra_charge)
        ) * self.quality
    

"""
