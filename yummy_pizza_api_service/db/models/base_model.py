from tortoise import fields, models


class BaseModel(models.Model):
    """Model for demo purpose."""

    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    

    def __str__(self) -> str:
        return self.name
