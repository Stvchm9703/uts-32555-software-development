from typing import List, Optional, Union, Any
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
# from yummy_pizza_api_service.db.models.receipt_model import OrderType, OrderStatus, OrderDeliveryType, OrderReceipt
# from yummy_pizza_api_service.db.models.transaction_model import Transaction
# from yummy_pizza_api_service.db.models.order_product_model import OrderProduct
from yummy_pizza_api_service.utils.datetime_str import convert_datetime_to_iso_8601_with_z_suffix

from yummy_pizza_api_service.web.api.product.schema import ProductOptionModelDTO, ProductModelDTO, ProductModelInputDTO, ProductOptionInputModelDTO
from datetime import datetime

class OPTransactionDTO(BaseModel):
    transaction_date: Optional[datetime]
    payment_type: Optional[str]
    payment_status: Optional[str]
    value: Optional[float]
    transaction_reference: Optional[str]

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }


class OrderProductOptionDTO(BaseModel):
    id: Optional[int]
    option: Optional[str]
    count: Optional[int]
    charge: Optional[float]
    option_referance: Optional[ProductOptionInputModelDTO]


class OrderProductDTO(BaseModel):
    id: Optional[int]
    quality: Optional[int]
    base_referance: Optional[ProductModelInputDTO]
    extra_options: Optional[List[OrderProductOptionDTO]]
    remark: Optional[str]


class OrderRefProductDTO(BaseModel):
    id: Optional[int]
    order_number: Optional[int]
    quality: Optional[int]
    product: Optional[ProductModelInputDTO]
    extra_options: Optional[List[OrderProductOptionDTO]]
    remark: Optional[str]


class OrderDTO(BaseModel):
    id: int
    contact_type: str
    status: str
    deliver_type: str

    customer_name: str
    customer_contact: int
    customer_address: str

    order_number: int
    staff: str
    items: Optional[List[OrderProductDTO]]

    transaction: Optional[OPTransactionDTO]


class OrderInputDTO(BaseModel):
    id: Optional[int]
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
