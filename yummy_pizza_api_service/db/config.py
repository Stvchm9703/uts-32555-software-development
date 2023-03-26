from databases import Database

from yummy_pizza_api_service.settings import settings

database = Database(str(settings.db_url))

