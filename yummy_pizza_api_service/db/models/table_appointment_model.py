from typing import Optional
import ormar
from datetime import datetime

from yummy_pizza_api_service.db.base import BaseModel, BaseMeta
from yummy_pizza_api_service.db.models.transaction_model import TransactionModel


class table_appointment_model(BaseModel):
    """
    the order record for front-counter/app creating order
    """
    appointment_reference: str = ormar.String(max_length=120)
    
    customer_name: str = ormar.String(max_length=500)
    customer_contact: int = ormar.Integer()
    customer_address: str = ormar.String(max_length=500)
    people_count: int = ormar.Integer()

    staff: str = ormar.String()
    timeslot: datetime = ormar.DateTime()
    transaction: Optional[TransactionModel] = ormar.ForeignKey(TransactionModel)

    class Meta(BaseMeta):
        """
        database meta
        """
        tablename = "order"
