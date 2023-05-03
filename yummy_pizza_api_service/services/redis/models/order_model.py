# from functools import reduce
# from enum import Enum
# from datetime import datetime
# from typing import Optional, List
# import json

# from redis.asyncio import Redis
# # from redis.connection import ConnectionPool

# from pydantic import BaseModel, PrivateAttr

# from yummy_pizza_api_service.db.models.receipt_model import OrderType, OrderStatus, OrderDeliveryType, OrderReceipt
# from yummy_pizza_api_service.db.models.transaction_model import Transaction

# from yummy_pizza_api_service.web.api.order.schema import OrderProductDTO
# from yummy_pizza_api_service.services.redis.models.order_product_model import OrderProduct

# from yummy_pizza_api_service.utils.merge import merge_model

# from hashids import Hashids


# class Order(BaseModel):
#     """
#     the order record for front-counter/app creating order
#     """
#     id: str
#     created_date: datetime = datetime.now()
#     updated_date: datetime = datetime.now()
#     contact_type: OrderType
#     status: OrderStatus = OrderStatus.created
#     deliver_type: OrderDeliveryType

#     customer_name: str
#     customer_contact: int
#     customer_address: str

#     order_number: int
#     #  TODO : implement the staff model
#     staff: str
#     items: Optional[List[OrderProduct]]

#     transaction: Optional[Transaction]

#     _order_prod_hash: Hashids = PrivateAttr()

#     @property
#     def values(self) -> float:
#         if self.transaction is None and len(self.items) == 0:
#             return 0.0
#         if self.transaction is not None:
#             return self.transaction.value
#         if self.items is not None and len(self.items) > 0:
#             return reduce((lambda x, y: x.value + y), self.items)
#         else:
#             return 0.0

#     # ======================================================
#     # oop lifecycle

#     def __init__(self, **data) -> None:
#         super().__init__(**data)
#         self._order_prod_hash = Hashids('OrderModel', 6)

#     # ======================================================
#     # # item related

#     def gen_item_id_hash(self) -> str:
#         return self._order_prod_hash.encode(self.id, len(self.items), int(datetime.now().timestamp()))

#     def add_item(self, item: OrderProductDTO) -> bool:
#         """
#         ## add_item 
#         to add the product item referancing to menu and add to item list (this order list)

#         ### !REMARK : Checking the product is valid, should be refer to controller / api handler
#         this items list check should related the list object data within program data but not 
#         any data related to database 
#         """
#         if item.product == None:
#             raise "referencing_product_is_empty"
#             return False

#         if item.product.is_available == False:
#             raise "product_is_not_available"
#             return False

#         if self.items is None:
#             self.items = []

#         new_item = OrderProduct(**item.dict())
#         new_item.id = self.gen_item_id_hash()
#         self.items.add(new_item)
#         return True

#     def get_item(self, target_item: OrderProductDTO = None) -> OrderProduct:
#         if target_item is None:
#             raise "required_item_is_empty"

#         if self.items == None or len(self.items) == 0:
#             raise "item_list_is_empty"

#         if target_item.id == None or target_item.id == 0:
#             raise "unknown_referance"

#         for item in (self.items):
#             if item.id == target_item.id:
#                 return item

#         return None

#     def update_item(self, edited_item: OrderProductDTO = None) -> bool:
#         try:
#             ore = self.get_item(edited_item)
#             if ore == None:
#                 return False
#             if edited_item.quality > ore.quality and ore.is_available:
#                 item = merge_model(item, edited_item)
#                 return True
#         except:
#             # unhandle case
#             return False

#     def remove_item(self, target_item: OrderProductDTO = None) -> bool:
#         tar_item = self.get_item(target_item)
#         if tar_item == None:
#             raise "request_item_is_not_exist"
#         self.items.remove(tar_item)
#         return True

#     # ======================================================

#     def update_status(self, status: str) -> bool:
#         try:
#             self.status = OrderStatus[status]
#             return True
#         except:
#             return False

#     def request_payment(self) -> bool:
#         return

#     def print_as_receipt(self) -> str:
#         """
#         for the customer to review and keep record
#         """
#         return ""

#     def convert_to_receipt(self) -> OrderReceipt:
#         return OrderReceipt(
#             contect_type=self.contact_type.value,
#             status=self.status.value,
#             deliver_type=self.deliver_type.value,

#             customer_name=self.customer_name,
#             customer_contact=self.customer_contact,
#             customer_address=self.customer_address,

#             staff=self.staff,
#             # remark=self.remark
#             order_snapshot=json.dumps(self.items),
#             transaction=self.transaction,
#             value=self.values
#         )

#     def print_as_kitchan_order(self) -> str:
#         """
#         for the kitchan/waiter to handle food order, 
#         """

#         return ""

#     # async def snapshot(self, redis_service: Redis) -> bool:
#     #     await redis_service.set('order_set__{id}'.format(self.id), self.json())
#     #     return False

#     # async def resume(self, redis_service: Redis, id: str) -> bool:
#     #     snap = await redis_service.get('order_set__{id}'.format(id))
#     #     self = Order.construct(**snap)
#     #     return True
