from typing import List

from yummy_pizza_api_service.settings import settings

MODELS_MODULES: List[str] = [
    "yummy_pizza_api_service.db.models.dummy_model",
]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
