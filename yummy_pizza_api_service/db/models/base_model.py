from tortoise import fields, models


class BaseModel(models.Model):
    """Model for Basic feature."""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200)  # noqa: WPS432
    
    
    # def __str__(self) -> str:
    #     return self.name
