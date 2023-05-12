from functools import reduce
from enum import Enum
from typing import Optional, List
import ormar

from yummy_pizza_api_service.db.base import BaseModel, BaseMeta

# from yummy_pizza_api_service.db.models.order_product_model import OrderProduct
from datetime import datetime
from yummy_pizza_api_service.db.models.transaction_model import Transaction, TransactionStatus, PaymentType


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

    customer_name: str = ormar.String(max_length=500, nullable=True)
    customer_contact: int = ormar.Integer(nullable=True)
    customer_address: str = ormar.String(max_length=500, nullable=True)

    order_number: int = ormar.Integer(maximum=999, minimum=0)
    staff: str = ormar.String(max_length=200, nullable=True)

    transaction: Optional[Transaction] = ormar.ForeignKey(
        Transaction,
        name="fk_transaction",
        nullable=True
    )

    class Meta(BaseMeta):
        """
        database meta
        """
        tablename = "op_order"

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

    async def update_status(self, status: OrderStatus) -> bool:
        """
        Update the status of the order.

        :param status: The new status of the order.
        :type status: OrderStatus
        :return: True if the status was updated successfully, False otherwise.
        :rtype: bool
        :raises: Any exception that occurs during the update process.
        """
        try:
            self.status = status.value
            await self.update()
            return True
        except:
            return False

    async def request_payment(self) -> bool:
        """
        Creates a new transaction and updates the order with the new transaction.

        :returns: True if the order is successfully updated, False otherwise.
        :rtype: bool
        """
        new_trans = await Transaction.objects.create(
            transaction_date=datetime.now(),
            payment_type=PaymentType.cash.value,
            payment_status=TransactionStatus.unpaid.value,
            value=self.values,
            transaction_reference="",
            remark=""
        )
        self.transaction = new_trans
        d = (await self.save_related(follow=True, save_all=True))
        return d != None

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
