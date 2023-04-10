from typing import Optional
import ormar
from datetime import datetime

from yummy_pizza_api_service.db.base import BaseModel, BaseMeta
from yummy_pizza_api_service.db.models.transaction_model import Transaction


class TableAppointment(BaseModel):
    """
    the order record for front-counter/app creating order
    """
    __table_args__ = {'extend_existing': True}

    appointment_reference: str = ormar.String(max_length=120)

    customer_name: str = ormar.String(max_length=500)
    customer_contact: int = ormar.Integer()
    customer_address: str = ormar.String(max_length=500)
    people_count: int = ormar.Integer()

    staff: str = ormar.String(max_length=200)
    timeslot: datetime = ormar.DateTime()
    transaction: Optional[Transaction] = ormar.ForeignKey(
        Transaction, skip_reverse=True)

    class Meta(BaseMeta):
        tablename = "table_appointment"
