
from typing import List, Optional, Union, Any
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
# from yummy_pizza_api_service.db.models.receipt_model import OrderType, OrderStatus, OrderDeliveryType, OrderReceipt
# from yummy_pizza_api_service.db.models.transaction_model import Transaction
# from yummy_pizza_api_service.db.models.order_product_model import OrderProduct
from yummy_pizza_api_service.web.api.order.schema import OPTransactionDTO
from yummy_pizza_api_service.utils.datetime_str import convert_datetime_to_iso_8601_with_z_suffix
from datetime import datetime


class TableAppointment(BaseModel):
    id: Optional[int]
    appointment_reference: Optional[str]
    order_number: Optional[int]
    customer_name: Optional[str]
    customer_contact: Optional[int]
    customer_address: Optional[str]
    people_count: Optional[int]

    staff: Optional[str]
    timeslot_start: Optional[datetime]
    timeslot_end: Optional[datetime]
    transaction: Optional[OPTransactionDTO]

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }
