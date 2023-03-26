from functools import reduce

from product_option import ProductOption


class Product():
    name: str = ""
    item_type: str = ""
    kal: int = 0
    price_value: float = 0.0

    rate: float = 0.0
    addication_extra_options: list[ProductOption] = []

    def __str__(self) -> str:
        return "product:" + self.id

    @property
    def full_price_value(self) -> float:
        return self.price_value * (1 + self.rate) + reduce(
            (lambda x, y: x.extra_charge + y), self.addication_extra_options
        )

    @property
    def is_available(self) -> bool:
        return True