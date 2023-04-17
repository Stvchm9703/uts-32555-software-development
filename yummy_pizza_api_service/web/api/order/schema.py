from typing import List, Optional, Union
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from yummy_pizza_api_service.db.models.receipt_model import OrderType, OrderStatus, OrderDeliveryType, OrderReceipt
from yummy_pizza_api_service.db.models.transaction_model import Transaction
from yummy_pizza_api_service.services.redis.models.order_product_model import OrderProduct

from yummy_pizza_api_service.web.api.product.schema import ProductOptionModelDTO, ProductModelDTO, ProductModelInputDTO


class OrderProductOptionDTO(BaseModel):
    id: Optional[str]
    option: Optional[str]
    count: Optional[int]
    charge: Optional[float]
    option_referance: Optional[ProductOptionModelDTO]


class OrderProductDTO(BaseModel):
    id: Optional[str]
    quality: Optional[int]
    product: ProductModelInputDTO
    extra_option: Optional[List[OrderProductOptionDTO]]
    remark: Optional[str]


class OrderDTO(BaseModel):
    id: str
    # created_date: Optional[datetime]
    # updated_date: Optional[datetime]
    contact_type: str
    status: str
    deliver_type: str

    customer_name: str
    customer_contact: int
    customer_address: str

    order_number: int
    staff: str
    items: Optional[List[OrderProductDTO]]

    # transaction: Optional[Transaction]


class OrderInputDTO(BaseModel):
    id: Optional[str]
    contact_type: Optional[str]
    status: Optional[str]
    deliver_type: Optional[str]
    customer_name: Optional[str]
    customer_contact: Optional[int]
    customer_address: Optional[str]
    order_number: Optional[int]
    staff: Optional[str]
    items: Optional[List[OrderProductDTO]]

    # transaction: Optional[Transaction]
