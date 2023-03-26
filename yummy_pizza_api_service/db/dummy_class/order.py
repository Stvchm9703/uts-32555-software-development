from order_product import OrderProduct
from transaction import Transaction
from functools import reduce
from enum import Enum


class OrderType(Enum):
    walk_in = 0
    phone_in = 1
    online_system = 2

class OrderStatus(Enum):
    created = 0
    void = -1
    paid = 1
    unpaid = 2
    delivering = 3
    completed = 4

class OrderDeliveryType(Enum):
    dine_in = 0 
    take_away = 1
    remote_delivery = 2


class Order():

    order_type: OrderType = OrderType.walk_in

    order_status: OrderStatus = OrderStatus.created

    # deliver type: ["dine-in" , "remote-delivery"]
    deliver_type: OrderDeliveryType = OrderDeliveryType.dine_in

    customer_name: str = ""
    customer_contact: int = 0
    customer_address: str = ""

    # for human readable
    order_number: int = 0
    #  TODO : implement the staff model
    staff: str = ""
    items: list[OrderProduct] = []
    # TODO : implement the transection model
    transection: Transaction = None

    _values: float = 0.0

    def __str__(self) -> str:
        return "order:" + self.id

    @property
    def values(self) -> float:
        if self.transection is None and len(self.items) == 0:
            return 0.0
        elif self.transection is not None:
            return self.transection.value
        elif len(self.items) > 0:
            return reduce((lambda x, y: x.value + y), self.items)
        else:
            return 0.0

    def add_item(self, item):
        self.items.append(item)
        return True
    
    def request_payment(self) -> bool:
        return
    
    def print_as_receipt(self) -> str:
        return 

    def __init__(self, ) -> None:

        pass