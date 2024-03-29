from enum import Enum
from functools import reduce
from typing import Optional, List
import ormar
from yummy_pizza_api_service.db.base import BaseModel, BaseMeta
# from yummy_pizza_api_service.db.models.product_option_model import ProductOptionModel


class ProductType(Enum):
    single = 'single'
    combo_set = 'combo_set'
    side = 'side'
    discount = 'discount'


class Product(BaseModel):
    """
    ### Product Model: ###
    #### description : ####
        for display menu and product selection,
        not the order contain
    """

    __table_args__ = {'extend_existing': True}

    name: str = ormar.String(max_length=200)
    description: str = ormar.String(max_length=500)
    item_type: str = ormar.String(max_length=100, choices=list(ProductType))
    category: str = ormar.String(max_length=250)
    kal: float = ormar.Float(minimum=0)
    price_value: float = ormar.Float()
    rate: float = ormar.Float()

    class Meta(BaseMeta):
        tablename = "product"

    def is_available(self) -> bool:
        """
        to check the inventory have enough raw material items
        for the inventory system, it may use service that connect to inventory system 
        to check the inventory item is enough 
        """
        return True

    @property
    def full_price_value(self) -> float:
        """
        to calculate the full price
        """
        return (1 + self.rate) * self.price_value
