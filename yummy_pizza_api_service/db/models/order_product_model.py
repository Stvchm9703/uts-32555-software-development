
from typing import List, Optional
from functools import reduce
import ormar
from yummy_pizza_api_service.db.base import BaseMeta, BaseModel
from product_model import ProductModel
from product_option_model import ProductOptionModel


class OrderProduct(BaseModel):
    quality: int = ormar.Integer()
    base_referance: Optional[ProductModel] = ormar.ForeignKey(ProductModel)
    extra_options: Optional[List[ProductOptionModel]] = ormar.ManyToMany(ProductOptionModel)
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

    