from datetime import datetime
import ormar
from ormar import ModelMeta

from yummy_pizza_api_service.db.config import database
from yummy_pizza_api_service.db.meta import meta


class BaseMeta(ModelMeta):
    """Base metadata for models."""
    database = database
    metadata = meta
    

class BaseModel(ormar.Model):
    """Model for DBO base model, for inhert."""
    class Meta(BaseMeta):
        abstract = True
        tablename = "base_model"
        model_fields = {
            '_uuid': ormar.BaseField(nullable=True, skip_field=True)
        }

    _uuid: str = ormar.UUID(version=5)
    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    created_date: datetime.datetime = ormar.DateTime(
        autoincrement=True,
        default=datetime.datetime.now
    )
    updated_date: datetime.datetime = ormar.DateTime(
        autoincrement=True,
        default=datetime.datetime.now,
    )


@ormar.pre_update(BaseModel)
async def before_update(sender, instance: BaseModel, **kwargs):
    print(kwargs)
    instance.updated_date = datetime.datetime.now
