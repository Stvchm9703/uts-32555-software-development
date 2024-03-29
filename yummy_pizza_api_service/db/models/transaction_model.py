
from typing import List, Optional, Union
from functools import reduce
from datetime import datetime
from enum import Enum
import ormar
# from ormar import fields
from yummy_pizza_api_service.db.base import BaseMeta, BaseModel
# from yummy_pizza_api_service.db.models.receipt_model import OrderReceipt
# from yummy_pizza_api_service.db.models.table_appointment_model import TableAppointment


class TransactionStatus(Enum):
    unpaid = "unpaid"
    paid = "paid"
    fail_paid = "fail_paid"
    unknown = "unknown"


class PaymentType(Enum):
    cash = "cash"
    yedpay = "yedpay"
    paypel = "paypel"


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class Transaction(BaseModel):
    __table_args__ = {'extend_existing': True}
    
    transaction_date: datetime = ormar.DateTime(nullable=True)
    payment_type: str = ormar.String(max_length=200, choices=list(PaymentType))
    payment_status: str = ormar.String(max_length=200, choices=list(TransactionStatus))
    value: float = ormar.Float(nullable=True)
    transaction_reference: str = ormar.String(max_length=200, nullable=True)
    remark: str = ormar.String(max_length=500, nullable=True)

    class Meta(BaseMeta):
        tablename = "transaction"

        
    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }


    def complete_payment(self, t_payment_type: PaymentType = PaymentType.cash) -> bool:
        # self.payment_type = t_payment_type
        # if t_payment_type == PaymentType.cash:
        #     self.payment_status = TransactionStatus.paid
        #     return True
        # if t_payment_type == PaymentType.yedpay:
        #     try:
        #         self.payment_status = TransactionStatus.paid
        #         return True
        #     except:
        #         self.payment_status = TransactionStatus.unpaid
        #         return False
        # self.payment_status = TransactionStatus.unknown
        return False
