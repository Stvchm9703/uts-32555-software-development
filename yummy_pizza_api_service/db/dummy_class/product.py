from functools import reduce

from product_option import ProductOption


class Product():
    name: str = ""
    item_type: str = ""
    kal: int = 0
    price_value: float = 0.0

    rate: float = 0.0
    addication_extra_options: list[ProductOption] = []

    # def __str__(self) -> str:
    #     return "product:" + self.id

    @property
    def full_price_value(self) -> float:
        return self.price_value * (1 + self.rate) + reduce(
            (lambda x, y: x.extra_charge + y), self.addication_extra_options
        )

    
    def is_available(self) -> bool:
        """
        to check the inventory have enough raw material items
        for the inventory system, it may use 
        """
        return True