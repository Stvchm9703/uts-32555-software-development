from order_product import OrderProduct
from transaction import Transaction
from functools import reduce
from enum import Enum


# class OrderType(Enum):
#     walk_in = "walk_in"
#     phone_in = "phone_in"
#     online_system = "online_system"


# class OrderStatus(Enum):
#     created = "created"
#     void = "void"
#     paid = "paid"
#     unpaid = "unpaid"
#     delivering = "delivering"
#     completed = "completed"


# class OrderDeliveryType(Enum):
#     dine_in = "dine_in"
#     take_away = "take_away"
#     remote_delivery = "remote_delivery"


class Order():

    order_type: str = ""


    order_status: str = ""

    # deliver type: ["dine-in" , "remote-delivery"]
    deliver_type: str = ""

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

    def __init__(self, **kwarg):
        if kwarg['customer_name']:
            self.customer_name = kwarg['customer_name']

        

    def add_items(self, item: OrderProduct) -> bool:
        """
        ## add_item 
        to add the product item referancing to menu and add to item list (this order list)
        """
        if item.base_referance == None:
            raise "referencing_product_is_empty"
            return False
        if item.quality == 0 or item.base_referance.is_available == False or item.base_referance.is_available == False:
            return False

        self.items.append(item)
        return True

    def update_item(self, edited_item: OrderProduct = None) -> bool:
        """
        ## update_item
        to update the product item within this order list
        """
        return True

    def remove_item(self, target_item: OrderProduct = None) -> bool:
        return True

    def request_payment(self) -> Transaction:
        return None

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
