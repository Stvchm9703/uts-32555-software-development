from fastapi import Depends
from redis.asyncio import ConnectionPool
from strawberry.fastapi import BaseContext

from yummy_pizza_api_service.services.redis.dependency import get_redis_pool


class Context(BaseContext):
    """Global graphql context."""

    def __init__(
        self,
        redis_pool: ConnectionPool = Depends(get_redis_pool),
    ) -> None:
        self.redis_pool = redis_pool
        pass  # noqa: WPS420


def get_context(context: Context = Depends(Context)) -> Context:
    """
    Get custom context.

    :param context: graphql context.
    :return: context
    """
    return context
