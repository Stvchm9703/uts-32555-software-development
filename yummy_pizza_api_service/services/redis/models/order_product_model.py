
from typing import List, Optional
from functools import reduce

from pydantic import BaseModel

from yummy_pizza_api_service.db.models.product_model import Product
from yummy_pizza_api_service.services.redis.models.order_product_option_model import OrderProductOption


class OrderProduct(BaseModel):
    quality: int 
    extra_option : Optional[List[OrderProductOption]]
    remark: str
    def total_charge(self) -> float:
        total_extra_charge = [x.extra_charge for x in self.extra_options]

        return float(
            self.base_referance.price_value
            + reduce((lambda x, y: x + y), total_extra_charge)
        ) * self.quality
    
