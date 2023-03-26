from enum import Enum
from functools import reduce


class TransactionStatus(str, Enum):
    unpaid = "unpaid"
    paid = "paid"
    fail_paid = "fail_paid"
    unknown = "unknown"

class PaymentType(str, Enum):
    cash = "cash"
    yedpay = "yedpay"

class Transaction():
    transaction_date = ""
    payment_type: PaymentType 
    payment_status: TransactionStatus = TransactionStatus.unpaid
    _value: float = 0.0

    @property
    def value(self) -> float:
        return self._value

    def request_payment(self, t_payment_type:PaymentType= PaymentType.cash) -> bool:
        self.payment_type = t_payment_type
        if t_payment_type == PaymentType.cash:
            self.payment_status = TransactionStatus.paid
            return True
        if t_payment_type == PaymentType.yedpay:
            try:
                self.payment_status = TransactionStatus.paid
                return True
            except:
                self.payment_status = TransactionStatus.unpaid
                return False
        self.payment_status = TransactionStatus.unknown
        return False
