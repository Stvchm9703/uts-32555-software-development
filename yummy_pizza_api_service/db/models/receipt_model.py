from typing import List, Optional
from enum import Enum
from functools import reduce
import json
import ormar
import pydantic
# from pydantic.json import pydantic_encoder
from yummy_pizza_api_service.db.base import BaseMeta, BaseModel
# from yummy_pizza_api_service.db.models.product_model import Product
# from yummy_pizza_api_service.db.models.product_option_model import ProductOption
from yummy_pizza_api_service.db.models.transaction_model import Transaction

# from yummy_pizza_api_service.services.redis.models.order_model import OrderProduct


class OrderType(Enum):
    walk_in = "walk_in"
    phone_in = "phone_in"
    online_system = "online_system"


class OrderStatus(Enum):
    created = "created"
    void = "void"
    paid = "paid"
    unpaid = "unpaid"
    producing = "producing"
    delivering = "delivering"
    completed = "completed"


class OrderDeliveryType(Enum):
    dine_in = "dine_in"
    take_away = "take_away"
    remote_delivery = "remote_delivery"


class OrderReceipt(BaseModel):
    """
    archive data model 
    """
    __table_args__ = {'extend_existing': True}
    contact_type: str = ormar.String(max_length=250, choices=list(OrderType))
    status: str = ormar.String(max_length=250, choices=list(OrderStatus))
    deliver_type: str = ormar.String(max_length=250, choices=list(OrderDeliveryType))

    customer_name: str = ormar.String(max_length=500)
    customer_contact: int = ormar.Integer()
    customer_address: str = ormar.String(max_length=500)
    staff: str = ormar.String(max_length=200)
    remark: str = ormar.String(max_length=500)
    order_snapshot: Optional[pydantic.Json] = ormar.JSON(nullable=True)
    transaction: Optional[Transaction] = ormar.ForeignKey(Transaction, skip_reverse=True)
    value : float = ormar.Float()
    
    # _order_list: Optional[List[OrderProduct]] = ormar.I

    class Meta(BaseMeta):
        tablename = "order_receipt"


    # @setattr(order_snapshot)
    # def set_order_list(self, item_list:str) -> bool:
    #     try:
    #         self.order_snapshot = item_list
    #         temp=json.loads(item_list)
    #         self._order_list = [OrderProduct.parse_obj(x) for x in temp]
    #         return True

    #     except Exception:
    #         return False

    # @setattr(order_snapshot)
    # def set_order_list(self, item_list: str) -> bool:
    #     try:
    #         self.order_snapshot = item_list
    #         temp = json.loads(item_list)
    #         self._order_list = [OrderProduct.parse_obj(x) for x in temp]
    #         return True

    #     except Exception:
    #         return False
