from functools import reduce


class Transaction():
    transaction_date = ""
    payment_type: str = ""
    payment_status: str = ""
    _value: float = 0.0

    @property
    def value(self) -> float:
        return self._value

    def request_payment(self, t_payment_type="cash") -> bool:
        self.payment_type = t_payment_type
        if t_payment_type == "cash":
            self.payment_status = "paid"
            return True
        if t_payment_type == "yedpay":
            try:
                self.payment_status = "paid"
                return True
            except:
                self.payment_status = "fail_paid"
                return False
        self.payment_status = "unknowed"
        return False
