
# from typing import List, Optional
# # from yummy_pizza_api_service.db.base import BaseMeta, BaseModel
# from pydantic import BaseModel
# from yummy_pizza_api_service.db.models.product_model import Product
# from yummy_pizza_api_service.db.models.product_option_model import ProductOption

# from yummy_pizza_api_service.services.redis.models.order_product_model import OrderProduct


# class OrderProductOption(BaseModel):
#     id: str
#     option: str
#     count: int
#     charge: float
#     option_referance: Optional[ProductOption]
    
#     @property
#     def opt_refer(self) -> int:
#         return self.option_referance.id or None
    

#     def to_receipt_str(self) -> str:
#         return ""