from order_product import OrderProduct
from transaction import Transaction
from functools import reduce

class Order():

    # order type : ["walk-in" , "phone-in", "online-system"]
    order_type: str = ""

    # order status : ["created", "void" , "payed" , "unpay" , "delivering" , "completed"]
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

    def add_item(self, item):
        self.items.append(item)
        return True
    
    def request_payment(self) -> bool:
        return
    
    def print_as_receipt(self) -> str:
        return 

    def __init__(self, ) -> None:

        pass