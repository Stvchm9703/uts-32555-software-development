from datetime import datetime
import ormar
from yummy_pizza_api_service.db.base import BaseMeta


class DummyModel(ormar.Model):
    """Model for demo purpose."""

    class Meta(BaseMeta):
        tablename = "dummy_model"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=200)  # noqa: WPS432
    updated_date: datetime = ormar.DateTime(
        autoincrement=True,
        default=datetime.now,
    )