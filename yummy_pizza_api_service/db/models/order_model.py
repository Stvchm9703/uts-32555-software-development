from functools import reduce
from enum import Enum
from typing import Optional, List
import ormar

from yummy_pizza_api_service.db.base import BaseModel, BaseMeta

from yummy_pizza_api_service.db.models.order_product_model import OrderProduct
from yummy_pizza_api_service.db.models.transaction_model import Transaction as Transaction


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


class Order(BaseModel):
    """
    the order record for front-counter/app creating order
    """
    __table_args__ = {'extend_existing': True}

    contact_type: str = ormar.String(max_length=250, choices=list(OrderType))
    status: str = ormar.String(max_length=250, choices=list(OrderStatus))
    deliver_type: str = ormar.String(max_length=250, choices=list(OrderDeliveryType))

    customer_name: str = ormar.String(max_length=500)
    customer_contact: int = ormar.Integer()
    customer_address: str = ormar.String(max_length=500)

    order_number: int = ormar.Integer(maximum=999, minimum=0)
    #  TODO : implement the staff model
    staff: str = ormar.String(max_length=200)
    # items: Optional[List[OrderProduct]] = ormar.ManyToMany(
    #     OrderProduct,
    #     name="fk_items_orderproduct"
    # )

    transaction: Optional[Transaction] = ormar.ForeignKey(
        Transaction,
        name="fk_transaction",
    )

    class Meta(BaseMeta):
        """
        database meta
        """
        tablename = "order"

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

    def print_as_kitchan_order(self) -> str:
        """
        for the kitchan/waiter to handle food order,
        """

        return ""

    def snapshot(self) -> bool:
        return False
