from product import Product
from product_option import ProductOption
from functools import reduce


class OrderProduct():
    quality: int = 0
    base_referance: Product = None
    extra_options: list[ProductOption] = []
    # @property
    def total_charge(self) -> float:
        # await self.fetch_related()
        total_extra_charge = [x.extra_charge for x in self.extra_options]

        return float(
            self.base_referance.price_value
            + reduce((lambda x, y: x + y), total_extra_charge)
        ) * self.quality
