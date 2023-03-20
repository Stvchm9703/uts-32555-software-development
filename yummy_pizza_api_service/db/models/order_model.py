from tortoise import fields, models
from tortoise import fields
from functools import reduce
import base_model
from product_model import ProductModel, ProductOptionModel


class OrderProductModel(base_model.BaseModel):
    quality = fields.IntField()
    base_referance: fields.ForeignKeyRelation[ProductModel] = fields.ForeignKeyField(
        "models.ProductModel", related_name="id"
    )
    extra_options: fields.ManyToManyRelation[ProductOptionModel] = fields.ForeignKeyField(
        "models.ProductOptionModel", related_name="id"
    )

    @property
    async def total_charge(self) -> float:
        await self.fetch_related()
        return float(
            self.base_referance.price_value
            + reduce((lambda x, y: x.extra_charge + y), self.extra_options)
        ) * self.quality


class OrderModel(base_model.BaseModel):

    # order type : ["walk-in" , "phone-in", "online-system"]
    order_type = fields.IntEnumField()

    # order status : ["created", "void" , "payed" , "unpay" , "delivering" , "completed"]
    order_status = fields.IntEnumField()

    # deliver type: ["dine-in" , "remote-delivery"]
    deliver_type = fields.IntEnumField()

    customer_name = fields.CharField(max_length=200)
    customer_contact = fields.IntField()
    customer_address = fields.CharField(max_length=500)

    # for human readable
    order_number = fields.IntField()
    #  TODO : implement the staff model
    staff = fields.CharField(max_length=200)
    items: fields.ManyToManyRelation[OrderProductModel] = fields.ManyToManyField("")
    # TODO : implement the transection model
    transection = fields.IntField()

    _values = fields.FloatField()

    def __str__(self) -> str:
        return "order:" + self.id

    @property
    def values(self) -> float:
        if self.transection is None and len(self.items) == 0:
            return 0.0
        elif self.transection is not None:
            return self.transection.value
        elif len(self.items) > 0:
            return reduce((lambda x, y: x.value + y), self.items)
        else:
            return 0.0


class OrderModel():

    # order type : ["walk-in" , "phone-in", "online-system"]
    order_type: str = ""

    # order status : ["created", "void" , "payed" , "unpay" , "delivering" , "completed"]
    order_status: str = ""

    # deliver type: ["dine-in" , "remote-delivery"]
    deliver_type: str = ""

    customer_name: str = ""
    customer_contact: int = 0
    customer_address: str = ""

    # for human readable
    order_number: int = 0
    #  TODO : implement the staff model
    staff: str = ""
    items: list[OrderProductModel] = []
    # TODO : implement the transection model
    transection: str = ""

    _values : float = 0.0

    def __str__(self) -> str:
        return "order:" + self.id

    @property
    def values(self) -> float:
        if self.transection is None and len(self.items) == 0:
            return 0.0
        elif self.transection is not None:
            return self.transection.value
        elif len(self.items) > 0:
            return reduce((lambda x, y: x.value + y), self.items)
        else:
            return 0.0



