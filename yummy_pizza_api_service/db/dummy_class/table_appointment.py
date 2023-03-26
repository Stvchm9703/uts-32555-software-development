from functools import reduce
from datetime import datetime
from transaction import Transaction

class TableAppointment():
    customer_name: str = ""
    customer_contact: int = 0
    customer_address: str = ""
    people_count: int = 0
    timeslot : datetime = datetime.now
    transection: Transaction = None

