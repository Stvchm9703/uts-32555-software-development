from tortoise import fields
from functools import reduce
import base_model
from inventory_item_model import InventoryItemModel
RATE = 0.045


class ProductOptionModel(base_model.BaseModel):
    name = fields.CharEnumField(max_length=200)
    extra_charge = fields.FloatField()
    option_kind = fields.CharEnumField()
    max_count = fields.IntField()
    min_count = fields.IntField()
    cost_items: fields.ManyToManyRelation[InventoryItemModel] = fields.ForeignKeyField(
        "models.InventoryItemModel", related_name="require_items", to_field="id"
    )


class ProductModel(base_model.BaseModel):
    """Model for demo purpose."""
    name = fields.CharField(max_length=200)
    item_type = fields.CharEnumField
    kal = fields.IntField
    # require item: reference to invetory item
    price_value = fields.IntField

    require_items: fields.ManyToManyRelation[InventoryItemModel] = fields.ForeignKeyField(
        "models.InventoryItemModel", related_name="require_items", to_field="id"
    )

    extra_options: fields.ForeignKeyNullableRelation[ProductOptionModel] = fields.ForeignKeyField(
        "models.ProductOptionModel", related_name="extra_options", to_field="id"
    )

    class Meta:
        table = "product"
        indexes = (('id'))

    def __str__(self) -> str:
        return "product:" + self.id

    # @property
    def get_full_price_value(self) -> float:
        return self.price_value * (1 + RATE)

    # @property
    async def get_cost_price_value(self) -> float:
        # await self.fetch_related('require_items')
        await self.require_items.all()
        return reduce((lambda x, y: x.cost + y), self.require_items)
