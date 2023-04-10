from functools import reduce
from enum import Enum
from typing import Optional, List
import json
from pydantic import BaseModel

from yummy_pizza_api_service.db.models.receipt_model import OrderType, OrderStatus, OrderDeliveryType, OrderReceipt
from yummy_pizza_api_service.db.models.transaction_model import Transaction;
from yummy_pizza_api_service.services.redis.models.order_product_model import OrderProduct

class Order(BaseModel):
    """
    the order record for front-counter/app creating order
    """
  
    contact_type: OrderType
    status: OrderStatus
    deliver_type: OrderDeliveryType

    customer_name: str
    customer_contact: int
    customer_address: str

    order_number: int
    #  TODO : implement the staff model
    staff: str
    items: Optional[List[OrderProduct]]

    transaction: Optional[Transaction] 


    def __str__(self) -> str:
        return "order:" + self.id

    def __json__(self) -> str:
        return
    # the object method

    @property
    def values(self) -> float:
        if self.transaction is None and len(self.items) == 0:
            return 0.0
        if self.transaction is not None:
            return self.transaction.value
        if self.items is not None and len(self.items) > 0:
            return reduce((lambda x, y: x.value + y), self.items)
        else:
            return 0.0

    # # item related
    async def add_items(self, item: OrderProduct) -> bool:
        """
        ## add_item 
        to add the product item referancing to menu and add to item list (this order list)
        """
        if item.base_referance == None:
            raise "referencing_product_is_empty"
            return False
        if item.quality == 0 or item.base_referance.is_available == False or item.base_referance.is_available == False:

            return False

        if self.items is None:
            self.items = List[OrderProduct]
        await self.items.add(item)
        return True

    async def update_item(self, edited_item: OrderProduct = None) -> bool:
        if edited_item is None:
            raise "required_item_is_empty"
            return False
        target_update = self.items.filter(id=edited_item.id).get()
        if len(target_update) == 0:
            raise "required_item_is_not_existed"
            return False

        await self.items.filter(id=edited_item.id).update(edited_item)
        # await self.save_related(relation_field=["items"])
        return True

    async def remove_item(self, target_item: OrderProduct = None) -> bool:
        if target_item is None:
            raise "required_item_is_empty"
            return False

        target_update = self.items.filter(id=target_item.id).get()
        if len(target_update) == 0:
            raise "required_item_is_not_existed"
            return False

        await self.items.remove(id=target_item.id)
        return True

    async def update_status(self, status: OrderStatus) -> bool:
        try:
            self.status = status.value
            await self.save()
            return True
        except:
            return False

    def request_payment(self) -> bool:
        return

    def print_as_receipt(self) -> str:
        """
        for the customer to review and keep record
        """
        return ""

    def convert_to_receipt(self) -> OrderReceipt:
        return OrderReceipt(
            contect_type=self.contact_type.value,
            status=self.status.value,
            deliver_type=self.deliver_type.value,

            customer_name=self.customer_name,
            customer_contact=self.customer_contact,
            customer_address=self.customer_address,

            staff=self.staff,
            # remark=self.remark
            order_snapshot= json.dumps(self.items),
            transaction=self.transaction,
            value=self.values
        )
      
    def print_as_kitchan_order(self) -> str:
        """
        for the kitchan/waiter to handle food order, 
        """

        return ""

    def snapshot(self) -> bool:
        return False
