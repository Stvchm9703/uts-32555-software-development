from ormar import ModelMeta

from yummy_pizza_api_service.db.config import database
from yummy_pizza_api_service.db.meta import meta


class BaseMeta(ModelMeta):
    """Base metadata for models."""

    database = database
    metadata = meta
    
